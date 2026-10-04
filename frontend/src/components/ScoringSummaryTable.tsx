import Avatar from "./Avatar";
import { type ScoringSummary, type User } from "../lib/api";

interface ScoringSummaryTableProps {
  scoringSummary: ScoringSummary;
  users: User[];
}

export default function ScoringSummaryTable({ scoringSummary, users }: ScoringSummaryTableProps) {
  if (scoringSummary.owners.length === 0) return null;

  return (
    <div className="scoring-summary-table-wrap">
      <table className="sortable-table">
        <thead>
          <tr>
            <th>Player</th>
            {scoringSummary.leagues.map((lg) => (
              <th key={lg}>{lg}</th>
            ))}
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {scoringSummary.owners.map((o) => (
            <tr key={o.user_id}>
              <td>
                <span className="player-link">
                  <Avatar
                    name={o.display_name}
                    src={users.find((u) => u.id === o.user_id)?.avatar_data_url}
                    size={22}
                  />
                  {o.display_name}
                </span>
              </td>
              {scoringSummary.leagues.map((lg) => (
                <td key={lg} className="points-cell">
                  {o.by_league[lg]?.toFixed(0) ?? 0}
                </td>
              ))}
              <td className="points-cell">
                <strong>{o.total.toFixed(0)}</strong>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
