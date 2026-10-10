import { useState } from "react";
import { type YesterdaysResult } from "../lib/api";

interface YesterdaysResultsCardProps {
  results: YesterdaysResult[];
}

function formatChange(change: number | null): string {
  if (change === null) return "";
  const sign = change > 0 ? "+" : "";
  return `${sign}${change.toFixed(2)} pts`;
}

function changeClass(change: number | null): string {
  if (change === null || change === 0) return "";
  return change > 0 ? "yesterdays-results-gain" : "yesterdays-results-loss";
}

function groupByLeague(results: YesterdaysResult[]): [string, YesterdaysResult[]][] {
  const byLeague = new Map<string, YesterdaysResult[]>();
  for (const r of results) {
    const list = byLeague.get(r.league);
    if (list) list.push(r);
    else byLeague.set(r.league, [r]);
  }
  return [...byLeague.entries()].sort((a, b) => a[0].localeCompare(b[0]));
}

export default function YesterdaysResultsCard({ results }: YesterdaysResultsCardProps) {
  const [collapsedLeagues, setCollapsedLeagues] = useState<Set<string>>(new Set());

  const toggleLeague = (league: string) => {
    setCollapsedLeagues((prev) => {
      const next = new Set(prev);
      if (next.has(league)) next.delete(league);
      else next.add(league);
      return next;
    });
  };

  const leagues = groupByLeague(results);

  return (
    <div className="yesterdays-results">
      <h3 className="scoring-summary-heading">Yesterday's Results</h3>
      {leagues.length === 0 ? (
        <p className="crib-value-note">No results to report yet.</p>
      ) : (
        leagues.map(([league, leagueResults]) => {
          const expanded = !collapsedLeagues.has(league);
          return (
            <div key={league} className="league-block">
              <button
                type="button"
                className="league-caret"
                onClick={() => toggleLeague(league)}
                aria-expanded={expanded}
                title={expanded ? "Collapse" : "Expand"}
              >
                <span className={expanded ? "caret-icon open" : "caret-icon"}>▸</span>
                <span className="league-name">{league}</span>
                <span className="crib-league-count">({leagueResults.length})</span>
              </button>
              {expanded && (
                <ul className="yesterdays-results-list">
                  {leagueResults.map((r, i) => {
                    const homeWon = r.home_score > r.away_score;
                    const awayWon = r.away_score > r.home_score;
                    return (
                      <li key={i} className="yesterdays-results-row">
                        <div className="todays-games-row yesterdays-results-matchup">
                          <span className="todays-games-matchup">
                            <strong className={homeWon ? "yesterdays-results-winner" : undefined}>
                              {r.home_team_name}
                            </strong>
                            {r.home_owner && <span className="todays-games-owner"> ({r.home_owner})</span>}
                            {" "}
                            {r.home_score}
                            {" – "}
                            {r.away_score}{" "}
                            <strong className={awayWon ? "yesterdays-results-winner" : undefined}>
                              {r.away_team_name}
                            </strong>
                            {r.away_owner && <span className="todays-games-owner"> ({r.away_owner})</span>}
                          </span>
                        </div>
                        {(r.home_owner || r.away_owner) && (
                          <div className="yesterdays-results-changes">
                            {r.home_owner && (
                              <span className={changeClass(r.home_point_change)}>
                                {r.home_owner}: {r.home_point_change === null ? "pending" : formatChange(r.home_point_change)}
                              </span>
                            )}
                            {r.home_owner && r.away_owner && <span className="yesterdays-results-sep">·</span>}
                            {r.away_owner && (
                              <span className={changeClass(r.away_point_change)}>
                                {r.away_owner}: {r.away_point_change === null ? "pending" : formatChange(r.away_point_change)}
                              </span>
                            )}
                          </div>
                        )}
                      </li>
                    );
                  })}
                </ul>
              )}
            </div>
          );
        })
      )}
    </div>
  );
}
