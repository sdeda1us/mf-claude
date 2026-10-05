import { type TodaysGame } from "../lib/api";

interface TodaysGamesCardProps {
  games: TodaysGame[];
}

export default function TodaysGamesCard({ games }: TodaysGamesCardProps) {
  return (
    <div className="todays-games">
      <h3 className="scoring-summary-heading">Today's Games</h3>
      {games.length === 0 ? (
        <p className="crib-value-note">No games scheduled today.</p>
      ) : (
        <ul className="todays-games-list">
          {games.map((g, i) => (
            <li key={i} className="todays-games-row">
              <span className="pill todays-games-league">{g.league}</span>
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
}
