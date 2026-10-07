# Daily results data drop

`latest.json` is written by the "Megafantasy Daily Score Sync" scheduled
Claude Code routine (claude.ai/code/routines), alongside its existing
`data/daily-sync/latest.json` and `data/daily-games/latest.json`
commits, then read and ingested by the backend's `daily_sync_pull_loop`
(`backend/app/daily_sync_pull.py`'s `pull_and_sync_results`).

Same sandboxed-egress reasoning as `../daily-sync/README.md` -- the
routine commits here instead of POSTing directly, since it can push to
GitHub but can't reach `megafantasy.win`.

This reports the FINAL SCORE of the previous day's games -- i.e. the
games that were in `../daily-games/latest.json` as of the last run,
before that file gets overwritten with today's schedule. The routine
reads the old content first, resolves each game's result, writes it
here, and only then overwrites `daily-games/latest.json` with today's
schedule.

Shape:
```json
{
  "date": "2026-10-06",
  "results": [
    {
      "league": "NFL",
      "home_team": "Kansas City Chiefs",
      "away_team": "Las Vegas Raiders",
      "home_score": 27,
      "away_score": 20
    }
  ]
}
```

Same 7-league scope as `../daily-games/README.md` (NFL, NBA, NHL, EPL,
UCL, URC, NCAAF). Matched against an existing `ScheduledGame` row by
(league, home_team, away_team) for the given date -- a result with no
matching schedule row is skipped (see
`backend/app/daily_results_sync.py`), not inserted, since there'd be no
owner information to attach to it.

`date` is `null` and `results` is `[]` until the routine is updated to
populate this file for real -- the backend treats that as "nothing to
report" rather than an error, same as `daily-games/latest.json`'s
placeholder convention.

This is pure data, not something to hand-edit -- it's expected to be
overwritten by the next routine run. Nothing reads any content other
than the current `main` HEAD, so history here isn't meaningful either.
