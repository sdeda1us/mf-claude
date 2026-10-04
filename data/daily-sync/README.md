# Daily sync data drop

`latest.json` is written by the "Megafantasy Daily Score Sync" scheduled
Claude Code routine (claude.ai/code/routines) once a day, then read and
ingested by the backend's `daily_sync_pull_loop`
(`backend/app/daily_sync_pull.py`).

The routine runs in a sandboxed cloud environment whose outbound network
access is restricted to a small fixed allowlist (Anthropic's own APIs,
package registries) — it cannot reach `megafantasy.win` directly to POST
its results. It commits here instead, since pushing to this repo (which
it already clones to read `season_labels.py`/`docs/wiki/`/`CLAUDE.md`) is
a different path than the HTTPS egress proxy that blocks everything else.
The backend — an ordinary Railway service with normal, unrestricted
internet access, unlike the sandbox — pulls this file on its own schedule
instead of waiting for a push it could never receive directly.

Shape: the same body `POST /api/scoring-sync/batch` takes —
`{"entries": [{"league": "...", "team": "...", "stats": {...}}, ...]}`.

This is pure data, not something to hand-edit — it's expected to be
overwritten by the next routine run. Nothing reads any content other
than the current `main` HEAD, so history here isn't meaningful either.
