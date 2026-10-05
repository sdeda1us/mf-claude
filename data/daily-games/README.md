# Daily games data drop

`latest.json` is written by the "Megafantasy Daily Score Sync" scheduled
Claude Code routine (claude.ai/code/routines) once a day, alongside its
existing `data/daily-sync/latest.json` commit, then read and ingested by
the backend's `daily_sync_pull_loop`
(`backend/app/daily_sync_pull.py`'s `pull_and_sync_games`).

Same sandboxed-egress reasoning as `../daily-sync/README.md` -- the
routine commits here instead of POSTing directly, since it can push to
GitHub but can't reach `megafantasy.win`.

Shape:
```json
{
  "date": "2026-10-05",
  "games": [
    {
      "league": "NFL",
      "home_team": "Kansas City Chiefs",
      "away_team": "Las Vegas Raiders",
      "venue": "GEHA Field at Arrowhead Stadium",
      "time_label": "8:15 PM ET"
    }
  ]
}
```

Scoped to the 7 leagues in `backend/app/routers/seasons.py`'s
`TODAYS_GAMES_LEAGUES` (NFL, NBA, NHL, EPL, UCL, URC, NCAAF) -- ATP/WTA
are deliberately excluded, since those are country/individual-match
aggregates with no single "team vs team" game to report. `venue` and
`time_label` are optional, best-effort free text -- `time_label` is
never parsed or validated by the backend, just displayed as-is.

`date` is `null` and `games` is `[]` until the routine is updated to
populate this file for real -- the backend treats that as "no games
today" rather than an error, so the Home page's widget just shows its
empty state in the meantime.

This is pure data, not something to hand-edit -- it's expected to be
overwritten by the next routine run. Nothing reads any content other
than the current `main` HEAD, so history here isn't meaningful either.
