import { Fragment, useEffect, useMemo, useState } from "react";
import { api, type ExampleScoreRow } from "../lib/api";

type SortKey = "points" | "team_name" | "league";
type SortDir = "asc" | "desc";

function csvField(value: string | number): string {
  const s = String(value);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

// Breakdown labels carry a per-team count for readability in the UI, e.g.
// "Wins (16)" — strip that trailing "(...)" to get a stable column name
// ("Wins") shared across every team that has a same-named scoring piece,
// regardless of league.
function componentName(label: string): string {
  return label.replace(/\s*\([^)]*\)\s*$/, "");
}

function downloadExampleScoresCsv(rows: ExampleScoreRow[]) {
  const componentNames = new Set<string>();
  for (const row of rows) {
    for (const piece of row.breakdown) {
      componentNames.add(componentName(piece.label));
    }
  }
  const components = Array.from(componentNames).sort((a, b) => a.localeCompare(b));

  const header = ["Team", "League", "Season", "Total Points", ...components];
  const lines = [header.map(csvField).join(",")];

  for (const row of rows) {
    const pointsByComponent = new Map(row.breakdown.map((p) => [componentName(p.label), p.points]));
    const line = [
      row.team_name,
      row.league,
      row.season_label,
      row.points,
      ...components.map((c) => pointsByComponent.get(c) ?? ""),
    ];
    lines.push(line.map(csvField).join(","));
  }

  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "megafantasy-example-scores.csv";
  a.click();
  URL.revokeObjectURL(url);
}

export default function ExampleScores() {
  const [rows, setRows] = useState<ExampleScoreRow[] | null>(null);
  const [sortKey, setSortKey] = useState<SortKey>("points");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [expandedTeamIds, setExpandedTeamIds] = useState<Set<number>>(new Set());

  useEffect(() => {
    api.get<ExampleScoreRow[]>("/leagues/example-scores").then(setRows);
  }, []);

  const sorted = useMemo(() => {
    if (!rows) return [];
    const copy = [...rows];
    copy.sort((a, b) => {
      let cmp: number;
      if (sortKey === "points") cmp = a.points - b.points;
      else cmp = a[sortKey].localeCompare(b[sortKey]);
      return sortDir === "asc" ? cmp : -cmp;
    });
    return copy;
  }, [rows, sortKey, sortDir]);

  const toggleSort = (key: SortKey) => {
    if (key === sortKey) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir(key === "points" ? "desc" : "asc");
    }
  };

  const toggleExpanded = (teamId: number) => {
    setExpandedTeamIds((prev) => {
      const next = new Set(prev);
      if (next.has(teamId)) next.delete(teamId);
      else next.add(teamId);
      return next;
    });
  };

  const arrow = (key: SortKey) => (sortKey === key ? (sortDir === "asc" ? " ▲" : " ▼") : "");

  if (!rows) return <p className="page">Loading…</p>;

  return (
    <div className="page">
      <h1>Example Scores</h1>
      <p>
        What each team's fantasy score would have been under the current rules, based on their
        most recently completed real-world season. Click a row to see how its score breaks down
        piece by piece.
      </p>
      <div className="team-board-controls">
        <button type="button" onClick={() => downloadExampleScoresCsv(sorted)}>
          Download CSV
        </button>
      </div>
      <table className="sortable-table">
        <thead>
          <tr>
            <th></th>
            <th onClick={() => toggleSort("team_name")}>Team{arrow("team_name")}</th>
            <th onClick={() => toggleSort("league")}>League{arrow("league")}</th>
            <th>Season</th>
            <th onClick={() => toggleSort("points")}>Points{arrow("points")}</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((row) => {
            const expanded = expandedTeamIds.has(row.team_id);
            return (
              <Fragment key={row.team_id}>
                <tr
                  className="team-row"
                  onClick={() => toggleExpanded(row.team_id)}
                  style={{ cursor: "pointer" }}
                >
                  <td>
                    <span className={expanded ? "caret-icon open" : "caret-icon"}>▸</span>
                  </td>
                  <td>{row.team_name}</td>
                  <td>
                    <span className="pill">{row.league}</span>
                  </td>
                  <td>{row.season_label}</td>
                  <td>{row.points}</td>
                </tr>
                {expanded && (
                  <tr>
                    <td></td>
                    <td colSpan={4}>
                      {row.breakdown.length === 0 ? (
                        <p className="queue-empty">No scoring pieces contributed (score is 0).</p>
                      ) : (
                        <table className="crib-sheet-table">
                          <thead>
                            <tr>
                              <th>Scoring piece</th>
                              <th>Points</th>
                            </tr>
                          </thead>
                          <tbody>
                            {row.breakdown.map((piece, i) => (
                              <tr key={i}>
                                <td>{piece.label}</td>
                                <td className="points-cell">{piece.points}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      )}
                    </td>
                  </tr>
                )}
              </Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
