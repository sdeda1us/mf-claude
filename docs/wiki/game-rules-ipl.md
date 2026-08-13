# IPL (Indian Premier League) Game Rules

Each player owns **1 IPL team**. Points below accrue per owned team and
sum to that player's total IPL score for the season.

| Event                                            | Points |
|-----------------------------------------------------|--------|
| Regular-season win                                     | +10    |
| Regular-season tie / no-result                          | +5     |
| Per 0.1 of Net Run Rate (NRR)                              | +2     |
| Qualify for the playoffs (top 4)                             | +10    |
| Win a knockout-stage match (Qualifier/Eliminator)               | +15    |
| Reach the Final                                                   | +25    |
| Win the Final (champion)                                            | +40    |

Base scoring mirrors NFL's shape rather than the win-minus-loss style most
leagues here use: real IPL points, like real NFL standings, never
penalize a loss (2 pts a win, 1 for a tie/no-result, 0 for a loss under
the actual competition rules) — so this app doesn't subtract for losses
either, matching NFL's own non-punitive formula. A 14-game IPL season is
roughly NFL scale, too. Net Run Rate — cricket's real tiebreaker stat,
typically running about -1.5 to +1.5 in practice — stands in for a
differential term.

IPL's knockout stage is a "page playoff," not a clean single-elimination
bracket: Qualifier 1 (1st vs 2nd, winner goes straight to the Final),
Eliminator (3rd vs 4th, loser is out), Qualifier 2 (Q1's loser vs the
Eliminator's winner, winner reaches the Final via the back door). Rather
than naming individual rounds the way other leagues do, the bonuses track
the two things that actually matter here: winning any knockout-stage
match (worth the same whether it's a Qualifier or the Eliminator), and
reaching/winning the Final. Bonuses stack cumulatively.

Roster: 1 team per player, drawn from the full 10-team league (see
`CLAUDE.md`).
