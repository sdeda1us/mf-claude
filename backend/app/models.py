import enum
from datetime import datetime, timezone

from sqlalchemy import JSON, Enum, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SeasonStatus(str, enum.Enum):
    setup = "setup"
    active = "active"
    complete = "complete"


class AuctionStatus(str, enum.Enum):
    pending = "pending"
    live = "live"
    complete = "complete"


class AuctionItemStatus(str, enum.Enum):
    pending = "pending"
    active = "active"
    sold = "sold"


class RosterSource(str, enum.Enum):
    auction = "auction"
    commissioner_correction = "commissioner_correction"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(100))
    is_commissioner: Mapped[bool] = mapped_column(default=False)
    # A small image as a data: URL (e.g. "data:image/jpeg;base64,..."), resized
    # client-side before upload. No object storage is configured for this app
    # and Railway's container filesystem is ephemeral across deploys, so the
    # avatar is stored inline rather than as a file on disk.
    avatar_data_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    bids: Mapped[list["Bid"]] = relationship(back_populates="user")
    roster_entries: Mapped[list["RosterEntry"]] = relationship(back_populates="user")


class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    # Fall and spring auctions each draw from their own separate budget —
    # spending in one session's leagues never eats into the other's.
    fall_budget_per_user: Mapped[float] = mapped_column(Numeric(10, 2), default=400)
    spring_budget_per_user: Mapped[float] = mapped_column(Numeric(10, 2), default=240)
    status: Mapped[SeasonStatus] = mapped_column(
        Enum(SeasonStatus), default=SeasonStatus.setup
    )
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    auctions: Mapped[list["Auction"]] = relationship(back_populates="season")
    roster_entries: Mapped[list["RosterEntry"]] = relationship(back_populates="season")


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    league: Mapped[str] = mapped_column(String(50))  # e.g. NFL, NBA, EPL
    sport: Mapped[str] = mapped_column(String(50))  # e.g. Football, Basketball, Soccer
    name: Mapped[str] = mapped_column(String(100))
    # A pre-computed expected-value dollar price (see app/set_ev_defaults.py),
    # shown as the crib sheet's starting value until a user overrides it with
    # their own CribSheetEntry. Null until that script has priced the team
    # (currently the 10 fall-session leagues only).
    default_value: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)

    __table_args__ = (UniqueConstraint("league", "name", name="uq_team_league_name"),)


class TeamSeasonResult(Base):
    __tablename__ = "team_season_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    league: Mapped[str] = mapped_column(String(50))
    season_label: Mapped[str] = mapped_column(String(20))  # e.g. "2025" or "2025-26"
    stats: Mapped[dict] = mapped_column(JSON)  # league-specific shape, see league_rules.compute_score

    team: Mapped["Team"] = relationship()

    __table_args__ = (
        UniqueConstraint("team_id", "season_label", name="uq_team_season_result"),
    )


class Auction(Base):
    __tablename__ = "auctions"

    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    # A season's roster is drafted in two separate auctions rather than one —
    # see docs/wiki/README.md's "Auction Sessions" section. Only teams whose
    # league is in that same session (app.league_rules.LEAGUE_SESSION) can be
    # nominated into this auction.
    session: Mapped[str] = mapped_column(String(10), default="fall")
    status: Mapped[AuctionStatus] = mapped_column(
        Enum(AuctionStatus), default=AuctionStatus.pending
    )
    # Shuffled once at auction creation; whose turn it is to nominate cycles
    # through this list, indexed by how many items have been nominated so far.
    nomination_order: Mapped[list[int]] = mapped_column(JSON, default=list)
    # Reset to "now" whenever a new nomination turn opens (auction created, an
    # item sells, or a nomination is cancelled) — the anchor the nomination
    # auto-nominate countdown is measured from.
    turn_started_at: Mapped[datetime] = mapped_column(default=utcnow)
    # Commissioner-only freeze: while true, nominating/bidding/passing are all
    # rejected and the in-flight countdown (nomination or bidding, whichever
    # applies) is frozen rather than just left running in the background.
    is_paused: Mapped[bool] = mapped_column(default=False)
    # When the current pause began — used on resume to shift whichever
    # deadline was running forward by exactly how long the pause lasted, so
    # paused time never counts against the clock.
    paused_at: Mapped[datetime | None] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    season: Mapped["Season"] = relationship(back_populates="auctions")
    items: Mapped[list["AuctionItem"]] = relationship(
        back_populates="auction", order_by="AuctionItem.order"
    )


class AuctionItem(Base):
    __tablename__ = "auction_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    auction_id: Mapped[int] = mapped_column(ForeignKey("auctions.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    order: Mapped[int] = mapped_column(default=0)
    status: Mapped[AuctionItemStatus] = mapped_column(
        Enum(AuctionItemStatus), default=AuctionItemStatus.pending
    )
    winning_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    winning_bid: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    # Bidding on this item closes when this passes — BID_TIMEOUT_SECONDS from
    # nomination, reset to exactly BID_EXTENSION_SECONDS from "now" by any
    # bid placed with under BID_EXTENSION_THRESHOLD_SECONDS left (a
    # soft-close / anti-sniping extension) — see auction_timer.py.
    bid_deadline: Mapped[datetime | None] = mapped_column(nullable=True, default=None)
    # Users who've declared they're out of bidding on this item. Once every
    # user except the current high bidder is in here, bidding ends
    # immediately rather than waiting for bid_deadline.
    passed_user_ids: Mapped[list[int]] = mapped_column(JSON, default=list)

    auction: Mapped["Auction"] = relationship(back_populates="items")
    team: Mapped["Team"] = relationship()
    bids: Mapped[list["Bid"]] = relationship(
        back_populates="item", order_by="Bid.created_at"
    )


class Bid(Base):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(primary_key=True)
    auction_item_id: Mapped[int] = mapped_column(ForeignKey("auction_items.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    item: Mapped["AuctionItem"] = relationship(back_populates="bids")
    user: Mapped["User"] = relationship(back_populates="bids")


class ReserveBid(Base):
    """A player's private standing "auto-top by $1" ceiling for one auction
    item — while active, resolve_reserve_bids() (auction_service.py) bids
    current_high + 1 on this user's behalf any time they're outbid, up to
    max_amount. Scoped to a single item; doesn't carry over to future
    nominations. One row per (item, user) — locking again just updates it."""

    __tablename__ = "reserve_bids"

    id: Mapped[int] = mapped_column(primary_key=True)
    auction_item_id: Mapped[int] = mapped_column(ForeignKey("auction_items.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    max_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    __table_args__ = (UniqueConstraint("auction_item_id", "user_id", name="uq_reserve_item_user"),)


class RosterEntry(Base):
    __tablename__ = "roster_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    price_paid: Mapped[float] = mapped_column(Numeric(10, 2))
    source: Mapped[RosterSource] = mapped_column(
        Enum(RosterSource), default=RosterSource.auction
    )
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    season: Mapped["Season"] = relationship(back_populates="roster_entries")
    user: Mapped["User"] = relationship(back_populates="roster_entries")
    team: Mapped["Team"] = relationship()


class QueueEntry(Base):
    """A team a player has queued up to bid on ahead of time. Consumed
    automatically by the nomination auto-nominate timeout, or bid on manually
    once it's the player's turn."""

    __tablename__ = "queue_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    order: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    team: Mapped["Team"] = relationship()

    __table_args__ = (
        UniqueConstraint("season_id", "user_id", "team_id", name="uq_queue_entry"),
    )


class CribSheetEntry(Base):
    """A player's own valuation of a team, for reference during any auction —
    not season-scoped, since it reflects the player's opinion of the team
    itself rather than anything about a particular draft."""

    __tablename__ = "crib_sheet_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    value: Mapped[float] = mapped_column(Numeric(10, 2))
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    team: Mapped["Team"] = relationship()

    __table_args__ = (
        UniqueConstraint("user_id", "team_id", name="uq_crib_sheet_entry"),
    )
