import { useState } from "react";
import { type YesterdaysResult, type YesterdaysScoringByPlayer } from "../lib/api";

interface YesterdaysResultsCardProps {
  results: YesterdaysResult[];
  scoringByPlayer: YesterdaysScoringByPlayer;
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

export default function YesterdaysResultsCard({
  results,
  scoringByPlayer,
}: YesterdaysResultsCardProps) {
  const [expandedOverrides, setExpandedOverrides] = useState<Map<string, boolean>>(new Map());

  const toggleLeague = (league: string, currentlyExpanded: boolean) => {
    setExpandedOverrides((prev) => {
      const next = new Map(prev);
      next.set(league, !currentlyExpanded);
      return next;
    });
  };

  const leagues = groupByLeague(results);

  return (
    <div className="yesterdays-results">
      {scoringByPlayer.owners.length > 0 && (
        <>
          <h3 className="scoring-summary-heading">Yesterday's Scoring by Player</h3>
          <div className="scoring-summary-table-wrap">
            <table className="sortable-table">
              <thead>
                <tr>
                  <th>Player</th>
                  {scoringByPlayer.leagues.map((lg) => (
                    <th key={lg}>{lg}</th>
                  ))}
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                {scoringByPlayer.owners.map((o) => (
                  <tr key={o.user_id}>
                    <td>{o.display_name}</td>
                    {scoringByPlayer.leagues.map((lg) => (
                      <td key={lg} className={`points-cell ${changeClass(o.by_league[lg] ?? null)}`}>
                        {lg in o.by_league ? formatChange(o.by_league[lg]) : "—"}
                      </td>
                    ))}
                    <td className={`points-cell ${changeClass(o.total)}`}>
                      <strong>{formatChange(o.total)}</strong>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      <h3 className="scoring-summary-heading">Yesterday's Results</h3>
      {leagues.length === 0 ? (
        <p className="crib-value-note">No results to report yet.</p>
      ) : (
        leagues.map(([league, leagueResults]) => {
          const expanded = expandedOverrides.get(league) ?? false;
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
                <span className="crib-league-count">({leagueResults.length})</span>
              </button>
              {expanded && (
                <ul className="yesterdays-results-list">
                  {leagueResults.map((r, i) => {
                    const pending = r.home_score === null || r.away_score === null;
                    const homeWon = !pending && r.home_score! > r.away_score!;
                    const awayWon = !pending && r.away_score! > r.home_score!;
                    return (
                      <li key={i} className="yesterdays-results-row">
                        <div className="todays-games-row yesterdays-results-matchup">
                          <span className="todays-games-matchup">
                            <strong className={homeWon ? "yesterdays-results-winner" : undefined}>
                              {r.home_team_name}
                            </strong>
                            {r.home_owner && <span className="todays-games-owner"> ({r.home_owner})</span>}
                            {" "}
                            {pending ? (
                              <span className="yesterdays-results-pending">vs.</span>
                            ) : (
                              <>
                                {r.home_score}
                                {" – "}
                                {r.away_score}
                              </>
                            )}{" "}
                            <strong className={awayWon ? "yesterdays-results-winner" : undefined}>
                              {r.away_team_name}
                            </strong>
                            {r.away_owner && <span className="todays-games-owner"> ({r.away_owner})</span>}
                            {pending && <span className="yesterdays-results-pending"> (pending)</span>}
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
