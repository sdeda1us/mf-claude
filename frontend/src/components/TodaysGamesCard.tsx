import { useState } from "react";
import { type TodaysGame } from "../lib/api";
import { useIsNarrow } from "../lib/useIsNarrow";

interface TodaysGamesCardProps {
  games: TodaysGame[];
}

function groupByLeague(games: TodaysGame[]): [string, TodaysGame[]][] {
  const byLeague = new Map<string, TodaysGame[]>();
  for (const g of games) {
    const list = byLeague.get(g.league);
    if (list) list.push(g);
    else byLeague.set(g.league, [g]);
  }
  return [...byLeague.entries()].sort((a, b) => a[0].localeCompare(b[0]));
}

export default function TodaysGamesCard({ games }: TodaysGamesCardProps) {
  const isNarrow = useIsNarrow(760);
  const [expandedOverrides, setExpandedOverrides] = useState<Map<string, boolean>>(new Map());

  const toggleLeague = (league: string, currentlyExpanded: boolean) => {
    setExpandedOverrides((prev) => {
      const next = new Map(prev);
      next.set(league, !currentlyExpanded);
      return next;
    });
  };

  const leagues = groupByLeague(games);

  return (
    <div className="todays-games">
      <h3 className="scoring-summary-heading">Today's Games</h3>
      {leagues.length === 0 ? (
        <p className="crib-value-note">No games scheduled today.</p>
      ) : (
        leagues.map(([league, leagueGames]) => {
          const expanded = expandedOverrides.get(league) ?? !isNarrow;
          return (
            <div key={league} className="league-block">
              <button
                type="button"
                className="league-caret"
                onClick={() => toggleLeague(league, expanded)}
                aria-expanded={expanded}
                title={expanded ? "Collapse" : "Expand"}
              >
                <span className={expanded ? "caret-icon open" : "caret-icon"}>▸</span>
                <span className="league-name">{league}</span>
                <span className="crib-league-count">({leagueGames.length})</span>
              </button>
              {expanded && (
                <ul className="todays-games-list">
                  {leagueGames.map((g, i) => (
                    <li key={i} className="todays-games-row">
                      <span className="todays-games-matchup">
                        <strong>{g.home_team_name}</strong>
                        {g.home_owner && <span className="todays-games-owner"> ({g.home_owner})</span>}
                        {" vs "}
                        <strong>{g.away_team_name}</strong>
                        {g.away_owner && <span className="todays-games-owner"> ({g.away_owner})</span>}
                      </span>
                      {(g.venue || g.time_label) && (
                        <span className="todays-games-meta">
                          {[g.time_label, g.venue].filter(Boolean).join(" · ")}
                        </span>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          );
        })
      )}
    </div>
  );
}
