import asyncio
from collections import defaultdict
from collections.abc import Coroutine
from typing import Any

from fastapi import WebSocket

from app.schemas import AuctionStateOut


class ConnectionManager:
    """Tracks connected sockets per auction room and broadcasts state to them.

    Postgres remains the source of truth; a client that reconnects re-syncs
    via GET /auctions/{id}/state rather than trusting the socket alone.
    """

    def __init__(self) -> None:
        self._rooms: dict[int, set[WebSocket]] = defaultdict(set)
        # asyncio only holds a weak reference to a task once nothing else
        # points at it, so a fire-and-forget task (e.g. the auto-nominate
        # countdown) can otherwise get garbage-collected mid-sleep — keeping
        # a strong reference here until it finishes prevents that.
        self._background_tasks: set[asyncio.Task] = set()

    def spawn(self, coro: Coroutine[Any, Any, None]) -> None:
        task = asyncio.create_task(coro)
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

    async def connect(self, auction_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self._rooms[auction_id].add(websocket)

    def disconnect(self, auction_id: int, websocket: WebSocket) -> None:
        self._rooms[auction_id].discard(websocket)
        if not self._rooms[auction_id]:
            del self._rooms[auction_id]

    async def broadcast_state(self, auction_id: int, state: AuctionStateOut) -> None:
        message = {"type": "state", "data": state.model_dump(mode="json")}
        dead: list[WebSocket] = []
        for ws in self._rooms.get(auction_id, set()):
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(auction_id, ws)

    async def send_error(self, websocket: WebSocket, detail: str) -> None:
        await websocket.send_json({"type": "error", "detail": detail})


manager = ConnectionManager()
