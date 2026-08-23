import { Fragment, useEffect, useMemo, useState } from "react";
import TeamLink from "../components/TeamLink";
import { api, type ExampleScoreRow, type LeagueRules } from "../lib/api";

type SortKey = "points" | "team_name" | "league";
type SortDir = "asc" | "desc";
type Tab = "teams" | "scenarios";
type ScenarioKey = "best" | "median" | "worst";

interface ScenarioTeam {
  id: number;
  name: string;
  points: number;
}

interface LeagueScenario {
  league: string;
  cap: number;
  pool: number;
  points: Record<ScenarioKey, number>;
  teams: Record<ScenarioKey, ScenarioTeam[]>;
}

// For a league with `cap` roster slots and `n` teams ranked by score, pick
// the cap-sized window at the top, bottom, and centered on the middle of
// the ranking. If the whole pool is smaller than the cap, every scenario
// just uses the whole pool (there's nothing else to fill it with).
function scenarioWindows(sorted: ScenarioTeam[], cap: number): Record<ScenarioKey, ScenarioTeam[]> {
  const n = sorted.length;
  if (n <= cap) return { best: sorted, median: sorted, worst: sorted };
  const start = Math.floor((n - cap) / 2);
  return {
    best: sorted.slice(0, cap),
    median: sorted.slice(start, start + cap),
    worst: sorted.slice(n - cap),
  };
}

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

const SCENARIO_LABELS: Record<ScenarioKey, string> = {
  best: "Best",
  median: "Median",
  worst: "Worst",
};

export default function ExampleScores() {
  const [rows, setRows] = useState<ExampleScoreRow[] | null>(null);
  const [rules, setRules] = useState<LeagueRules | null>(null);
  const [sortKey, setSortKey] = useState<SortKey>("points");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [expandedTeamIds, setExpandedTeamIds] = useState<Set<number>>(new Set());
  const [leagueFilter, setLeagueFilter] = useState("");
  const [tab, setTab] = useState<Tab>("teams");
  const [expandedScenarioLeagues, setExpandedScenarioLeagues] = useState<Set<string>>(new Set());

  useEffect(() => {
    api.get<ExampleScoreRow[]>("/leagues/example-scores").then(setRows);
    api.get<LeagueRules>("/leagues/rules").then(setRules);
  }, []);

  const leagues = useMemo(() => {
    if (!rows) return [];
    return Array.from(new Set(rows.map((r) => r.league))).sort((a, b) => a.localeCompare(b));
  }, [rows]);

  const sorted = useMemo(() => {
    if (!rows) return [];
    const filtered = leagueFilter ? rows.filter((r) => r.league === leagueFilter) : rows;
    const copy = [...filtered];
    copy.sort((a, b) => {
      let cmp: number;
      if (sortKey === "points") cmp = a.points - b.points;
      else cmp = a[sortKey].localeCompare(b[sortKey]);
      return sortDir === "asc" ? cmp : -cmp;
    });
    return copy;
  }, [rows, sortKey, sortDir, leagueFilter]);

  const scenarios = useMemo<LeagueScenario[]>(() => {
    if (!rows || !rules) return [];
    const byLeague = new Map<string, ScenarioTeam[]>();
    for (const r of rows) {
      const list = byLeague.get(r.league) ?? [];
      list.push({ id: r.team_id, name: r.team_name, points: r.points });
      byLeague.set(r.league, list);
    }
    return Object.entries(rules.roster_limits)
      .filter(([league]) => byLeague.has(league))
      .map(([league, cap]) => {
        const sorted = [...(byLeague.get(league) ?? [])].sort(
          (a, b) => b.points - a.points || a.name.localeCompare(b.name)
        );
        const windows = scenarioWindows(sorted, cap);
        const points: Record<ScenarioKey, number> = {
          best: windows.best.reduce((sum, t) => sum + t.points, 0),
          median: windows.median.reduce((sum, t) => sum + t.points, 0),
          worst: windows.worst.reduce((sum, t) => sum + t.points, 0),
        };
        return { league, cap, pool: sorted.length, points, teams: windows };
      })
      .sort((a, b) => a.league.localeCompare(b.league));
  }, [rows, rules]);

  const scenarioTotals = useMemo(() => {
    const totals: Record<ScenarioKey, number> = { best: 0, median: 0, worst: 0 };
    for (const s of scenarios) {
      totals.best += s.points.best;
      totals.median += s.points.median;
      totals.worst += s.points.worst;
    }
    return totals;
  }, [scenarios]);

  const toggleScenarioLeague = (league: string) => {
    setExpandedScenarioLeagues((prev) => {
      const next = new Set(prev);
      if (next.has(league)) next.delete(league);
      else next.add(league);
      return next;
    });
  };

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

      <div className="session-tabs">
        <button
          type="button"
          className={tab === "teams" ? "session-tab current" : "session-tab"}
          onClick={() => setTab("teams")}
        >
          All Teams
        </button>
        <button
          type="button"
          className={tab === "scenarios" ? "session-tab current" : "session-tab"}
          onClick={() => setTab("scenarios")}
        >
          Roster Scenarios
        </button>
      </div>

      {tab === "teams" && (
        <>
          <div className="team-board-controls">
            <select value={leagueFilter} onChange={(e) => setLeagueFilter(e.target.value)}>
              <option value="">All leagues</option>
              {leagues.map((league) => (
                <option key={league} value={league}>
                  {league}
                </option>
              ))}
            </select>
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
                      <td>
                        <TeamLink teamId={row.team_id} league={row.league} name={row.team_name} />
                      </td>
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
        </>
      )}

      {tab === "scenarios" && (
        <>
          <p>
            If a player somehow filled every roster spot in a league with its <strong>best</strong>
            -scoring available teams, its <strong>median</strong> teams, or its{" "}
            <strong>worst</strong>-scoring teams — what would that add up to? Each league's window
            uses its real roster cap; click a league to see which teams landed in each scenario.
          </p>
          <div className="summary-strip">
            <div className="summary-stat">
              <span className="summary-value">{scenarioTotals.best.toLocaleString()}</span>
              <span className="summary-label">best full roster</span>
            </div>
            <div className="summary-stat">
              <span className="summary-value">{scenarioTotals.median.toLocaleString()}</span>
              <span className="summary-label">median full roster</span>
            </div>
            <div className="summary-stat">
              <span className="summary-value">{scenarioTotals.worst.toLocaleString()}</span>
              <span className="summary-label">worst full roster</span>
            </div>
          </div>
          <table className="sortable-table">
            <thead>
              <tr>
                <th></th>
                <th>League</th>
                <th>Best</th>
                <th>Median</th>
                <th>Worst</th>
              </tr>
            </thead>
            <tbody>
              {scenarios.map((s) => {
                const expanded = expandedScenarioLeagues.has(s.league);
                return (
                  <Fragment key={s.league}>
                    <tr
                      className="team-row"
                      onClick={() => toggleScenarioLeague(s.league)}
                      style={{ cursor: "pointer" }}
                    >
                      <td>
                        <span className={expanded ? "caret-icon open" : "caret-icon"}>▸</span>
                      </td>
                      <td>
                        <span className="pill">{s.league}</span> ({s.cap}/player, pool {s.pool})
                      </td>
                      <td className="points-cell">{s.points.best.toLocaleString()}</td>
                      <td className="points-cell">{s.points.median.toLocaleString()}</td>
                      <td className="points-cell">{s.points.worst.toLocaleString()}</td>
                    </tr>
                    {expanded && (
                      <tr>
                        <td></td>
                        <td colSpan={4}>
                          <div className="hero-gallery">
                            {(["best", "median", "worst"] as ScenarioKey[]).map((key) => (
                              <div key={key}>
                                <p className="crib-league-count">{SCENARIO_LABELS[key]}</p>
                                <table className="crib-sheet-table">
                                  <tbody>
                                    {s.teams[key].map((t) => (
                                      <tr key={t.id}>
                                        <td>
                                          <TeamLink teamId={t.id} league={s.league} name={t.name} />
                                        </td>
                                        <td className="points-cell">{t.points}</td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            ))}
                          </div>
                        </td>
                      </tr>
                    )}
                  </Fragment>
                );
              })}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}
