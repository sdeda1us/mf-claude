# Daily results data drop (retired)

This file is no longer read by anything. Yesterday's final scores for
the Home page's "Yesterday's Results" card now sync directly from
ESPN's API, backend-side -- see `backend/app/espn_results_sync.py` and
`backend/app/espn_client.py`'s module docstring for why (same reasoning
as `backend/app/nhl_standings_sync.py` bypassing the routine for NHL
standings: the routine's sandboxed egress can't reach ESPN at all, while
this backend has normal unrestricted outbound internet access and can
just fetch it directly -- with far better completeness than the
routine's old web-search step had).

The "Megafantasy Daily Score Sync" scheduled Claude Code routine no
longer needs to populate `latest.json` here. This folder (and this
README) are kept around as a historical note rather than deleted
outright; nothing breaks if `latest.json` is stale, missing, or removed.
