# Megafantasy

A private auction fantasy league app for a 6-person group: each season everyone gets a
$600 budget to bid on real sports teams in a live, real-time auction. Scoring rules are
not implemented yet — this is the auction + roster foundation.

- **Backend**: FastAPI + SQLAlchemy + Alembic, WebSocket-based live auction room
- **Frontend**: React + Vite + TypeScript
- **Auth**: passwordless magic-link email, restricted to a 6-email allow-list
- **Email**: Resend (falls back to logging the link to the console if unconfigured)

## Local development

Requires Docker (for Postgres) or just Python 3.11+ / Node 20+ if you'd rather run
against SQLite directly.

### Option A: docker-compose (Postgres, closest to production)

```bash
cp backend/.env.example backend/.env   # edit ALLOWED_EMAILS to your 6 real emails
docker compose up --build
```

Then in a second terminal, seed the users/teams and run the frontend:

```bash
docker compose exec backend python -m app.seed
cd frontend
cp .env.example .env
npm install
npm run dev
```

Visit http://localhost:5173.

### Option B: SQLite, no Docker

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit ALLOWED_EMAILS
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

### Logging in

With no `RESEND_API_KEY` set, magic links are printed to the backend console instead of
emailed — look for a line like:

```
RESEND_API_KEY not set — magic link for alice@example.com: http://localhost:8000/api/auth/verify?token=...
```

Paste that URL into your browser to log in as that user.

## Project layout

```
backend/    FastAPI app: models, auth, REST routers, the WebSocket auction room
frontend/   React app: login, seasons, live auction room, roster, commissioner tools
Dockerfile  combined build: bakes the frontend into the backend's static/ dir
docker-compose.yml   local dev: Postgres + backend (frontend runs separately via `npm run dev`)
```

See `backend/app/seed.py` for the seeded placeholder teams — replace with real league
data once you know which sports/teams you're drafting from.

## Deploying

**Recommended: Railway.**

1. Create a Railway project, add a Postgres plugin.
2. Add a service from this repo (it will build the root `Dockerfile`).
3. Set service env vars: `DATABASE_URL` (Railway's Postgres connection string, using the
   `postgresql+psycopg://` scheme), `JWT_SECRET` (long random string), `ALLOWED_EMAILS`,
   `RESEND_API_KEY`, `EMAIL_FROM`, `APP_BASE_URL` / `API_BASE_URL` (both = your Railway
   public URL, since frontend and backend are served from the same origin), `COOKIE_SECURE=true`.
4. Deploy. Then run the seed script once via Railway's shell/console:
   `python -m app.seed`.

Because the frontend is built into the backend's `static/` directory, it's a single
service with a single URL — no CORS or cross-site cookie configuration needed.

**Alternative:** Fly.io works just as well (also has solid WebSocket + Postgres
support) but needs a bit more manual setup (`fly.toml`, volumes) than Railway's
GitHub-connected auto-deploy.
