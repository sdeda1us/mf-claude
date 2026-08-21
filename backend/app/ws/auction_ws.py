from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.auction_service import (
    all_non_high_bidders_passed,
    auto_pass_capped_users,
    build_state,
    count_user_league_teams,
    count_user_minor_conference_teams,
    current_high_bid,
    finalize_active_item,
    get_active_item,
    high_bidder_user_id,
    remaining_budget_by_user,
    resolve_reserve_bids,
)
from app.auction_timer import (
    BID_EXTENSION_SECONDS,
    BID_EXTENSION_THRESHOLD_SECONDS,
    naive_utc,
    schedule_turn_timer,
)
from app.database import SessionLocal
from app.deps import get_user_from_websocket
from app.league_rules import MINOR_CONFERENCE_CAPS, ROSTER_LIMITS, is_minor_conference_team
from app.models import Auction, Bid, ReserveBid
from app.ws.connection_manager import manager

router = APIRouter()


@router.websocket("/ws/auction/{auction_id}")
async def auction_room(websocket: WebSocket, auction_id: int):
    db: Session = SessionLocal()
    try:
        user = get_user_from_websocket(websocket, db)
    except Exception:
        await websocket.close(code=4401)
        db.close()
        return

    auction = db.get(Auction, auction_id)
    if auction is None:
        await websocket.close(code=4404)
        db.close()
        return

    await manager.connect(auction_id, websocket, user.id)
    await websocket.send_json(
        {
            "type": "state",
            "data": build_state(db, auction, viewer_user_id=user.id).model_dump(mode="json"),
        }
    )

    try:
        while True:
            message = await websocket.receive_json()
            message_type = message.get("type")
            if message_type not in ("bid", "pass", "reserve"):
                await manager.send_error(websocket, "Unknown message type")
                continue

            # This connection's db session stays open for its whole lifetime,
            # so anything it already lazy-loaded (e.g. item.bids) would
            # otherwise keep reflecting stale data from before other users'
            # concurrent bids/passes committed on their own sessions —
            # expire everything so this message's reads hit the database.
            db.expire_all()
            if auction.is_paused:
                await manager.send_error(websocket, "Auction is paused")
                continue

            item = get_active_item(db, auction_id)
            if item is None:
                await manager.send_error(websocket, "No active item to bid on")
                continue

            if message_type == "pass":
                winner_id = high_bidder_user_id(item)
                if user.id == winner_id:
                    await manager.send_error(websocket, "You already have the high bid")
                    continue
                if user.id not in item.passed_user_ids:
                    item.passed_user_ids = [*item.passed_user_ids, user.id]
                    db.commit()
                await manager.broadcast_state(auction_id, db, auction)

                if all_non_high_bidders_passed(db, item):
                    finalize_active_item(db, auction, item)
                    db.commit()
                    db.refresh(auction)
                    await manager.broadcast_state(auction_id, db, auction)
                    manager.spawn(schedule_turn_timer(auction_id))
                continue

            if message_type == "reserve":
                if user.id in item.passed_user_ids:
                    await manager.send_error(
                        websocket, "You've passed on this team — you can't set a reserve on it"
                    )
                    continue

                active_flag = message.get("active")
                if not isinstance(active_flag, bool):
                    await manager.send_error(websocket, "Invalid reserve request")
                    continue

                existing = (
                    db.query(ReserveBid)
                    .filter(ReserveBid.auction_item_id == item.id, ReserveBid.user_id == user.id)
                    .first()
                )

                if not active_flag:
                    if existing is not None and existing.active:
                        existing.active = False
                        db.commit()
                    await manager.broadcast_state(auction_id, db, auction)
                    continue

                amount = message.get("amount")
                if not isinstance(amount, (int, float)) or amount <= 0:
                    await manager.send_error(websocket, "Invalid reserve amount")
                    continue

                high_bid = current_high_bid(item)
                if amount <= high_bid:
                    await manager.send_error(
                        websocket, f"Reserve must exceed current high bid of {high_bid}"
                    )
                    continue

                league = item.team.league
                limit = ROSTER_LIMITS.get(league)
                if limit is not None:
                    owned = count_user_league_teams(db, auction.season_id, user.id, league)
                    if owned >= limit:
                        await manager.send_error(
                            websocket,
                            f"You already own the maximum number of {league} teams ({limit})",
                        )
                        continue

                minor_cap = MINOR_CONFERENCE_CAPS.get(league)
                if minor_cap is not None and is_minor_conference_team(league, item.team.name):
                    minor_owned = count_user_minor_conference_teams(
                        db, auction.season_id, user.id, league
                    )
                    if minor_owned >= minor_cap:
                        await manager.send_error(
                            websocket,
                            f"You already own the maximum number of minor-conference {league} "
                            f"teams ({minor_cap})",
                        )
                        continue

                if existing is not None:
                    existing.max_amount = amount
                    existing.active = True
                else:
                    db.add(
                        ReserveBid(
                            auction_item_id=item.id,
                            user_id=user.id,
                            max_amount=amount,
                            active=True,
                        )
                    )
                db.commit()

                resolve_reserve_bids(
                    db,
                    auction,
                    item,
                    bid_extension_threshold_seconds=BID_EXTENSION_THRESHOLD_SECONDS,
                    bid_extension_seconds=BID_EXTENSION_SECONDS,
                )
                db.commit()

                await manager.broadcast_state(auction_id, db, auction)

                if all_non_high_bidders_passed(db, item):
                    finalize_active_item(db, auction, item)
                    db.commit()
                    db.refresh(auction)
                    await manager.broadcast_state(auction_id, db, auction)
                    manager.spawn(schedule_turn_timer(auction_id))
                continue

            if user.id in item.passed_user_ids:
                await manager.send_error(websocket, "You've passed on this team — you can't bid on it again")
                continue

            amount = message.get("amount")
            if not isinstance(amount, (int, float)) or amount <= 0:
                await manager.send_error(websocket, "Invalid bid amount")
                continue

            high_bid = current_high_bid(item)
            if amount <= high_bid:
                await manager.send_error(websocket, f"Bid must exceed current high bid of {high_bid}")
                continue

            remaining = remaining_budget_by_user(db, auction.season, auction.session).get(user.id, 0)
            if amount > remaining:
                await manager.send_error(websocket, f"Bid exceeds your remaining budget of {remaining}")
                continue

            league = item.team.league
            limit = ROSTER_LIMITS.get(league)
            if limit is not None:
                owned = count_user_league_teams(db, auction.season_id, user.id, league)
                if owned >= limit:
                    await manager.send_error(
                        websocket,
                        f"You already own the maximum number of {league} teams ({limit})",
                    )
                    continue

            minor_cap = MINOR_CONFERENCE_CAPS.get(league)
            if minor_cap is not None and is_minor_conference_team(league, item.team.name):
                minor_owned = count_user_minor_conference_teams(db, auction.season_id, user.id, league)
                if minor_owned >= minor_cap:
                    await manager.send_error(
                        websocket,
                        f"You already own the maximum number of minor-conference {league} teams ({minor_cap})",
                    )
                    continue

            new_bid = Bid(auction_item_id=item.id, user_id=user.id, amount=amount)
            item.bids.append(new_bid)
            db.add(new_bid)
            # Soft close: once under BID_EXTENSION_THRESHOLD_SECONDS remain,
            # any bid resets the clock back to exactly BID_EXTENSION_SECONDS
            # rather than extending from whatever was left, so late snipes
            # can't shrink the window.
            if item.bid_deadline is not None:
                now = datetime.utcnow()
                remaining_seconds = (naive_utc(item.bid_deadline) - now).total_seconds()
                if remaining_seconds < BID_EXTENSION_THRESHOLD_SECONDS:
                    item.bid_deadline = now + timedelta(seconds=BID_EXTENSION_SECONDS)
            # Anyone now at their roster cap for this league can't bid on it
            # again, so they're auto-passed rather than left to click Pass
            # on a team they're no longer eligible to win.
            auto_pass_capped_users(db, auction, item)
            # Anyone with an active reserve below the new high bid auto-tops
            # it by $1 (possibly cascading against a rival reserve) before
            # this settles — a locked reserve should react the same way a
            # human watching the auction would.
            resolve_reserve_bids(
                db,
                auction,
                item,
                bid_extension_threshold_seconds=BID_EXTENSION_THRESHOLD_SECONDS,
                bid_extension_seconds=BID_EXTENSION_SECONDS,
            )
            db.commit()

            await manager.broadcast_state(auction_id, db, auction)

            if all_non_high_bidders_passed(db, item):
                finalize_active_item(db, auction, item)
                db.commit()
                db.refresh(auction)
                await manager.broadcast_state(auction_id, db, auction)
                manager.spawn(schedule_turn_timer(auction_id))
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(auction_id, websocket)
        db.close()
