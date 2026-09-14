# UCL (UEFA Champions League) Game Rules

Each player owns **4 UCL teams**, drawn from the 36-club league phase field
(see `CLAUDE.md`). Points below accrue per owned team and sum to that
player's total UCL score for the season.

| Event                                                | Points |
|----------------------------------------------------------|--------|
| Per league phase point (win = 3 pts, draw = 1, loss = 0)    | +3     |
| Per goal of league phase goal differential (GD)              | +1     |
| Make the knockout phase (finish top 24 of 36)                  | +10    |
| Reach the Round of 16                                            | +10    |
| Reach the quarter-finals                                          | +10    |
| Reach the semi-finals                                               | +10    |
| Reach the final                                                       | +10    |
| Win the final                                                           | +10    |

The base is EPL-style (points + a goal-differential term), scaled up to 3
points per league-phase point instead of EPL's 2 — the league phase is
only 8 games long (versus a 38-game domestic season), so per-point value
needed to be higher for it to register at all. Knockout bonuses are a flat
+10 per round survived, halving the field each time: 36 clubs enter, 24
survive the league phase into the knockout structure (8 go straight to the
Round of 16, the other 16 play a two-legged playoff round for the
remaining 8 Round of 16 spots), then 16 → 8 → 4 → 2 → 1 champion. Bonuses
stack cumulatively — the champion banks all six.
