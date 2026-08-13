# Megafantasy Wiki

Game rules and scoring reference, one page per league. This is separate from
`CLAUDE.md`'s "Sports Leagues" section (team rosters / season dates) — this
wiki covers how points are actually scored once the season is underway.

All 19 leagues (MLB/NFL/NBA/NHL/EPL/NCAAF/NCAAMB/NCAAWB/ATP/WTA/PGA/LPGA/F1/
WNBA/MLS/URC/IPL/NWSL/TDF) have scoring and roster limits wired into the app
(`backend/app/league_rules.py`, the `/rules` page, roster caps enforced at
bid time) and `/example-scores` historical data
(`backend/app/seed_historical_results.py`). The 6 added after the original
6 (NCAAMB/NCAAWB/ATP/WTA/PGA/LPGA) have deliberately scoped-down historical
data given their scale — e.g. NCAAMB/NCAAWB only cover Sweet-16-or-better
teams rather than the full ~360-team pool; see that file's module docstring
and per-league comments for the exact scope of each. ATP/WTA/PGA/LPGA are
also structurally different from every other league: the draftable "team"
is a country (tennis) or a letter of the alphabet (golf), not a club — see
game-rules-tennis-mens.md and game-rules-pga.md for how that aggregation
works. F1's "team" is a constructor (a works team fielding two cars) — see
game-rules-f1.md; its historical backfill blends exact season totals (wins,
podiums, poles, fastest laps) with reasoned estimates for the harder-to-
source per-car points-finish counts, documented in that file's comments.
WNBA scoring mimics NBA's style but is scaled for a shorter (44-game),
conference-less season — see game-rules-wnba.md. MLS scoring blends EPL's
exact points+GD base with cumulative playoff-round bonuses (MLS has a
bracket, EPL doesn't) — see game-rules-mls.md. URC blends EPL's points+
differential base (rescaled — rugby's points-difference swings much wider
than a soccer goal differential) with WNBA-style 3-round playoff bonuses,
since URC has a knockout bracket EPL doesn't — see game-rules-urc.md. IPL
mirrors NFL's non-punitive base (no penalty for a loss, matching real
IPL/NFL points systems) plus Net Run Rate as the differential term, with
bonuses tracking IPL's "page playoff" knockout stage rather than named
rounds — see game-rules-ipl.md. NWSL scoring is EPL's points+GD base plus
WNBA/URC-style 3-round playoff bonuses (NWSL's playoff, like WNBA's, is a
single 8-team bracket with no conference stage) plus a Shield bonus
mirroring MLS's Supporters' Shield — see game-rules-nwsl.md. TDF (Tour de
France Team Classification) is structurally unlike every other league here:
it's a single once-a-year ranked outcome, not a season of games, so it uses
golf's placement-tiered scoring shape instead of anything win/loss-based —
see game-rules-tdf.md, which also flags that the 2027 Tour's actual team
rosters won't be formalized until ~January 2027, so the current team pool
(the 2026 Tour's 23 teams) is a placeholder pending re-verification.

## Game Seasons

A "game season" (the roster/auction cycle a `Season` row represents) runs
from the start of one EPL season to the start of the next — EPL is the
anchor because it's the only league whose kickoff reliably lands in the
same narrow window every year. Whichever real-world season or major
cycle a league's own next season **starts** inside that window is the one
that counts for that game season, even if it hasn't finished (or even
started) by the time the game season itself begins.

For leagues with no single opening day — ATP, WTA, PGA, LPGA all run as a
set of majors spread across the calendar rather than a single season —
the "start" is the first major of the calendar year: the Australian Open
for ATP/WTA, The Masters for PGA, The Chevron Championship for LPGA (the
first of the four majors the LPGA counts — see
[game-rules-lpga.md](game-rules-lpga.md) for why Evian is excluded).

Worked example — the game season running **Aug 21, 2026** (2026/27 EPL
kickoff) **→ next EPL kickoff (~Aug 2027, not yet officially dated)**:

| League | Real-world season that counts | Starts |
|---|---|---|
| EPL | 2026/27 | Aug 21, 2026 |
| NCAAF | 2026 | Aug 27, 2026 |
| NFL | 2026 | Sept 9, 2026 |
| NHL | 2026-27 | Sept 29, 2026 |
| URC | 2026-27 | ~late Sept 2026 (not yet officially scheduled) |
| NBA | 2026-27 | ~Oct 20, 2026 |
| NCAAMB / NCAAWB | 2026-27 | Nov 1, 2026 |
| ATP / WTA | 2027 (Australian Open → US Open) | ~Jan 2027 |
| MLB | 2027 | ~March 24-25, 2027 |
| F1 | 2027 (Australian GP → season finale) | ~March 2027 (not yet scheduled) |
| PGA | 2027 (The Masters → The Open) | ~April 2027 (not yet scheduled) |
| LPGA | 2027 (Chevron → AIG) | ~April 2027 (not yet scheduled) |
| WNBA | 2027 | ~May 2027 (not yet scheduled) |
| MLS | 2027 (new July-May calendar) | Mid-to-late July 2027 |
| IPL | 2027 | ~late March 2027 (not yet scheduled) |
| NWSL | 2027 | ~March 2027 (not yet scheduled) |
| TDF | 2027 | ~July 2027 (not yet scheduled; teams not formalized until ~Jan 2027) |

Note what this rule deliberately excludes from the current game season:
MLB 2026, F1 2026, WNBA 2026, and NWSL 2026 (all four already underway
before the window opens — NWSL 2026 started March 13, 2026), and the
2026 ATP/WTA/PGA/LPGA cycles (already substantially or fully complete) —
those belong to the *prior* game season instead. IPL 2026 is a related but
distinct case: unlike the other spring leagues, its entire 2026 season
(March 28 - May 31, 2026) already started *and finished* before the
window opens, so it's just as excluded, but for a stronger reason — IPL
seasons run start-to-finish within a single calendar year, so "IPL 2026"
is never split across two game-seasons the way MLB/F1/WNBA/NWSL's
2026 seasons are. TDF is its own case: the 2026 Tour de France (July
2026) already ran before the window opens too, so the *2027* Tour is what
counts here — same exclusion logic, just with the added wrinkle that
2027's team rosters aren't even formalized yet. Dates marked "not yet
scheduled" use the historical typical timing noted in `CLAUDE.md` and
should be re-verified once officially announced.

MLS is a special case worth calling out: the league is switching from a
Feb/March-December calendar to a July-May calendar starting in 2027, with
a one-off shortened "transition campaign" bridging the two (Feb-May 2027,
14 games, its own playoffs and MLS Cup) before the first full July-2027-
start season kicks off. That transition campaign technically starts
earlier in the window than the new July season does, but it's a one-time
bridge, not the new format — this app targets the new July-May calendar
going forward, so MLS's game-season entry is the July 2027 season, not
the transition campaign. Re-visit this if the transition campaign turns
out to need its own roster cycle.

## Auction Sessions

Each game season's auction is split into two sessions rather than run all
at once, so a league's roster is drafted reasonably close to when it's
actually being played:

- **Fall session** (~late August): EPL, NCAAF, NFL, NHL, NBA, NCAAMB,
  NCAAWB, ATP, WTA, URC
- **Spring session** (~March): MLB, PGA, LPGA, F1, WNBA, MLS, IPL, NWSL, TDF

The fall/spring grouping doesn't perfectly track each league's own season
start from the table above — it's a deliberate simplification, not a
by-product of it. NCAAMB/NCAAWB (season starts Nov 1) and ATP/WTA (season
effectively starts at the Australian Open, ~January) both start well after
the fall session drafts them; the alternative was drafting them in the
spring session instead, which would be worse (NCAAMB/NCAAWB: after the
regular season and into the tournament itself; ATP/WTA: after the
Australian Open, missing a major from the drafted season). Between "rosters
sit idle for a few months" and "rosters are set after the season's already
partly or mostly over," the fall session is the smaller problem for both.

## Leagues

- [MLB](game-rules-mlb.md)
- [NFL](game-rules-nfl.md)
- [NBA](game-rules-nba.md)
- [NHL](game-rules-nhl.md)
- [EPL](game-rules-epl.md)
- [NCAAF](game-rules-ncaaf.md)
- [NCAAMB](game-rules-ncaamb.md)
- [NCAAWB](game-rules-ncaawb.md)
- [ATP (Men's Tennis)](game-rules-tennis-mens.md)
- [WTA (Women's Tennis)](game-rules-tennis-womens.md)
- [PGA (Men's Golf)](game-rules-pga.md)
- [LPGA (Women's Golf)](game-rules-lpga.md)
- [F1 (Formula 1)](game-rules-f1.md)
- [WNBA](game-rules-wnba.md)
- [MLS](game-rules-mls.md)
- [URC (United Rugby Championship)](game-rules-urc.md)
- [IPL (Indian Premier League)](game-rules-ipl.md)
- [NWSL](game-rules-nwsl.md)
- [TDF (Tour de France Team Classification)](game-rules-tdf.md)
