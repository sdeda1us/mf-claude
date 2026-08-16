import asyncio
from collections import defaultdict
from collections.abc import Coroutine
from typing import Any

from fastapi import WebSocket
from sqlalchemy.orm import Session

from app.auction_service import build_state
from app.models import Auction


class ConnectionManager:
    """Tracks connected sockets per auction room and broadcasts state to them.

    Postgres remains the source of truth; a client that reconnects re-syncs
    via GET /auctions/{id}/state rather than trusting the socket alone.
    """

    def __init__(self) -> None:
        # websocket -> the user_id it authenticated as, so broadcasts can be
        # built per-viewer (e.g. reserve bids are private — each socket
        # should only ever see its own, never another user's).
        self._rooms: dict[int, dict[WebSocket, int]] = defaultdict(dict)
        # asyncio only holds a weak reference to a task once nothing else
        # points at it, so a fire-and-forget task (e.g. the auto-nominate
        # countdown) can otherwise get garbage-collected mid-sleep — keeping
        # a strong reference here until it finishes prevents that.
        self._background_tasks: set[asyncio.Task] = set()

    def spawn(self, coro: Coroutine[Any, Any, None]) -> None:
        task = asyncio.create_task(coro)
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

    async def connect(self, auction_id: int, websocket: WebSocket, user_id: int) -> None:
        await websocket.accept()
        self._rooms[auction_id][websocket] = user_id

    def disconnect(self, auction_id: int, websocket: WebSocket) -> None:
        self._rooms[auction_id].pop(websocket, None)
        if not self._rooms[auction_id]:
            del self._rooms[auction_id]

    async def broadcast_state(self, auction_id: int, db: Session, auction: Auction) -> None:
        dead: list[WebSocket] = []
        for ws, user_id in list(self._rooms.get(auction_id, {}).items()):
            try:
                state = build_state(db, auction, viewer_user_id=user_id)
                await ws.send_json({"type": "state", "data": state.model_dump(mode="json")})
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(auction_id, ws)

    async def send_error(self, websocket: WebSocket, detail: str) -> None:
        await websocket.send_json({"type": "error", "detail": detail})


manager = ConnectionManager()
