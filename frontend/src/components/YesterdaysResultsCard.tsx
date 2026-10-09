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

export default function YesterdaysResultsCard({ results }: YesterdaysResultsCardProps) {
  return (
    <div className="yesterdays-results">
      <h3 className="scoring-summary-heading">Yesterday's Results</h3>
      {results.length === 0 ? (
        <p className="crib-value-note">No results to report yet.</p>
      ) : (
        <ul className="yesterdays-results-list">
          {results.map((r, i) => {
            const homeWon = r.home_score > r.away_score;
            const awayWon = r.away_score > r.home_score;
            return (
              <li key={i} className="yesterdays-results-row">
                <div className="todays-games-row yesterdays-results-matchup">
                  <span className="pill todays-games-league">{r.league}</span>
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
}
