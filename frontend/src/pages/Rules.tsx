import { useEffect, useState } from "react";
import { api, type LeagueRules } from "../lib/api";

export default function Rules() {
  const [rules, setRules] = useState<LeagueRules | null>(null);

  useEffect(() => {
    api.get<LeagueRules>("/leagues/rules").then(setRules);
  }, []);

  if (!rules) return <p className="page">Loading…</p>;

  return (
    <div className="page">
      <h1>Scoring Rules</h1>
      {Object.entries(rules.scoring_rules).map(([league, lines]) => (
        <div key={league} className="rules-card">
          <div className="ribbon">{league}</div>
          <p className="rules-card-meta">
            <span className="pill">
              {rules.roster_limits[league]} team{rules.roster_limits[league] === 1 ? "" : "s"} per player
            </span>
          </p>
          <table>
            <tbody>
              {lines.map((line) => (
                <tr key={line.label}>
                  <td>{line.label}</td>
                  <td className="points-cell">
                    {line.points > 0 ? `+${line.points}` : line.points}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}
