from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.auction_service import current_turn_user_id, get_active_item
from app.auction_timer import schedule_bid_timer, schedule_turn_timer
from app.config import settings
from app.database import SessionLocal
from app.models import Auction, AuctionStatus
from app.routers import auction, auth, crib_sheet, leagues, queue, roster, seasons, teams, users
from app.ws import auction_ws
from app.ws.connection_manager import manager


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Turn and bid timers live only in memory (an asyncio task per open turn
    # or active item), so a restart — a deploy, a crash, anything — silently
    # drops whichever countdown was running. Without this, that turn/item
    # would just sit open forever with a countdown on screen that never
    # actually fires. A paused auction is left alone — resume() is what
    # re-arms its timer, using the frozen deadline it already has.
    db = SessionLocal()
    try:
        auctions = db.query(Auction).filter(Auction.status != AuctionStatus.complete).all()
        for a in auctions:
            if a.is_paused:
                continue
            item = get_active_item(db, a.id)
            if item is not None:
                manager.spawn(schedule_bid_timer(item.id))
            elif current_turn_user_id(db, a) is not None:
                manager.spawn(schedule_turn_timer(a.id))
    finally:
        db.close()
    yield


app = FastAPI(title="Megafantasy API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.app_base_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Namespaced under /api so backend routes never collide with frontend
# client-side page routes (e.g. the "/seasons/1/roster" page vs. the
# "GET /seasons/{id}/roster" endpoint used to share the same path).
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(seasons.router, prefix="/api")
app.include_router(teams.router, prefix="/api")
app.include_router(auction.router, prefix="/api")
app.include_router(roster.router, prefix="/api")
app.include_router(queue.router, prefix="/api")
app.include_router(crib_sheet.router, prefix="/api")
app.include_router(leagues.router, prefix="/api")
app.include_router(auction_ws.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}


# In the combined-deploy image, the built frontend is copied to backend/static.
# /assets is Vite's hashed JS/CSS bundle; everything else falls back to
# index.html so client-side routes (e.g. /seasons/1/roster) survive a
# hard refresh instead of 404ing against the API server.
static_dir = Path(__file__).resolve().parent.parent / "static"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="static-assets")

    @app.get("/{full_path:path}")
    def spa_fallback(full_path: str):
        candidate = static_dir / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(static_dir / "index.html")
