import { useEffect, useMemo, useState } from "react";
import { api, type ExampleScoreRow } from "../lib/api";

type SortKey = "points" | "team_name" | "league";
type SortDir = "asc" | "desc";

export default function ExampleScores() {
  const [rows, setRows] = useState<ExampleScoreRow[] | null>(null);
  const [sortKey, setSortKey] = useState<SortKey>("points");
  const [sortDir, setSortDir] = useState<SortDir>("desc");

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

  const arrow = (key: SortKey) => (sortKey === key ? (sortDir === "asc" ? " ▲" : " ▼") : "");

  if (!rows) return <p className="page">Loading…</p>;

  return (
    <div className="page">
      <h1>Example Scores</h1>
      <p>
        What each team's fantasy score would have been under the current rules, based on their
        most recently completed real-world season.
      </p>
      <table className="sortable-table">
        <thead>
          <tr>
            <th onClick={() => toggleSort("team_name")}>Team{arrow("team_name")}</th>
            <th onClick={() => toggleSort("league")}>League{arrow("league")}</th>
            <th>Season</th>
            <th onClick={() => toggleSort("points")}>Points{arrow("points")}</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((row) => (
            <tr key={row.team_id}>
              <td>{row.team_name}</td>
              <td>
                <span className="pill">{row.league}</span>
              </td>
              <td>{row.season_label}</td>
              <td>{row.points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
