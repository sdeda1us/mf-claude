import { useEffect, useMemo, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import PlayerRosterPanel from "../components/PlayerRosterPanel";
import ScoringSummaryTable from "../components/ScoringSummaryTable";
import { useChartPalette } from "../lib/chartPalette";
import Plot from "../lib/plotly";
import {
  api,
  type LeagueRules,
  type LeagueTeamScore,
  type LeagueWeeklyGain,
  type ScoringSummary,
  type Season,
  type User,
} from "../lib/api";

const TOP_WEEKLY_GAINERS = 5;

const STATUS_LABEL: Record<Season["status"], string> = {
  setup: "Setup",
  active: "Active",
  complete: "Complete",
};

export default function Seasons() {
  const { user: viewer } = useAuth();
  const palette = useChartPalette();
  const [seasons, setSeasons] = useState<Season[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [rules, setRules] = useState<LeagueRules | null>(null);
  const [selectedSeasonId, setSelectedSeasonId] = useState("");
  const [selectedUserId, setSelectedUserId] = useState("");
  const [selectedLeague, setSelectedLeague] = useState("");
  const [scoringSummary, setScoringSummary] = useState<ScoringSummary | null>(null);
  const [leagueTeamScores, setLeagueTeamScores] = useState<LeagueTeamScore[]>([]);
  const [weeklyGains, setWeeklyGains] = useState<LeagueWeeklyGain[]>([]);

  useEffect(() => {
    api.get<Season[]>("/seasons").then(setSeasons);
    api.get<User[]>("/users").then(setUsers);
    api.get<LeagueRules>("/leagues/rules").then(setRules);
  }, []);

  // Default to the active season the first time seasons load, falling back
  // to the most recent one if none is active.
  useEffect(() => {
    if (selectedSeasonId || seasons.length === 0) return;
    const active = seasons.find((s) => s.status === "active");
    setSelectedSeasonId(String((active ?? seasons[0]).id));
  }, [seasons, selectedSeasonId]);

  useEffect(() => {
    if (!selectedSeasonId) {
      setScoringSummary(null);
      return;
    }
    api.get<ScoringSummary>(`/seasons/${selectedSeasonId}/scoring-summary`).then(setScoringSummary);
  }, [selectedSeasonId]);

  // Default the player picker to whoever's logged in; if that can't be
  // determined, fall back to first place in the standings. Re-applied
  // every time the selected season changes.
  const defaultUserId = useMemo(() => {
    if (viewer) return String(viewer.id);
    if (scoringSummary && scoringSummary.owners.length > 0) {
      return String(scoringSummary.owners[0].user_id);
    }
    return "";
  }, [viewer, scoringSummary]);

  useEffect(() => {
    setSelectedUserId(defaultUserId);
  }, [selectedSeasonId, defaultUserId]);

  // Leagues actually being scored right now (see LeagueRules.active_leagues)
  // that this season also has a standings column for -- the options for the
  // "which league's breakdown" picker below the standings table.
  const activeLeagueOptions = useMemo(() => {
    if (!rules || !scoringSummary) return [];
    return rules.active_leagues.filter((lg) => scoringSummary.leagues.includes(lg));
  }, [rules, scoringSummary]);

  // Default to whichever active league currently has the most combined
  // points across every owner.
  const defaultLeague = useMemo(() => {
    if (!scoringSummary || activeLeagueOptions.length === 0) return "";
    let best = activeLeagueOptions[0];
    let bestTotal = -Infinity;
    for (const lg of activeLeagueOptions) {
      const total = scoringSummary.owners.reduce((sum, o) => sum + (o.by_league[lg] ?? 0), 0);
      if (total > bestTotal) {
        bestTotal = total;
        best = lg;
      }
    }
    return best;
  }, [activeLeagueOptions, scoringSummary]);

  useEffect(() => {
    setSelectedLeague(defaultLeague);
  }, [selectedSeasonId, defaultLeague]);

  useEffect(() => {
    if (!selectedSeasonId || !selectedLeague) {
      setLeagueTeamScores([]);
      return;
    }
    api
      .get<LeagueTeamScore[]>(`/seasons/${selectedSeasonId}/leagues/${selectedLeague}/team-scores`)
      .then(setLeagueTeamScores);
  }, [selectedSeasonId, selectedLeague]);

  useEffect(() => {
    if (!selectedSeasonId || !selectedLeague) {
      setWeeklyGains([]);
      return;
    }
    api
      .get<LeagueWeeklyGain[]>(`/seasons/${selectedSeasonId}/leagues/${selectedLeague}/weekly-gains`)
      .then(setWeeklyGains);
  }, [selectedSeasonId, selectedLeague]);

  // One color per owner, assigned in standings order, so an owner's color
  // means the same thing here as anywhere else on this page.
  const ownerColor = useMemo(() => {
    const color: Record<number, string> = {};
    (scoringSummary?.owners ?? []).forEach((o, i) => {
      color[o.user_id] = palette.owners[i % palette.owners.length];
    });
    return color;
  }, [scoringSummary, palette.owners]);

  // One Plotly trace per rostered team (not per owner) so each team is its
  // own stack segment, colored by its owner -- same "per-team trace,
  // shared owner color" pattern as Analytics' "Where the Money Went"
  // chart. Players are ranked ascending by total so the highest scorer
  // ends up at the top of the axis (Plotly stacks category arrays
  // bottom-to-top by default).
  const leagueChart = useMemo(() => {
    const totalByUser = new Map<number, number>();
    const nameByUser = new Map<number, string>();
    for (const row of leagueTeamScores) {
      totalByUser.set(row.user_id, (totalByUser.get(row.user_id) ?? 0) + row.points);
      nameByUser.set(row.user_id, row.display_name);
    }
    const players = Array.from(totalByUser.entries())
      .map(([userId, total]) => ({ userId, name: nameByUser.get(userId) ?? `User #${userId}`, total }))
      .sort((a, b) => a.total - b.total);

    const traces = leagueTeamScores.map((row) => ({
      type: "bar" as const,
      orientation: "h" as const,
      x: [row.points],
      y: [nameByUser.get(row.user_id) ?? row.display_name],
      name: row.team_name,
      showlegend: false,
      marker: {
        color: ownerColor[row.user_id] ?? palette.neutral,
        // A hairline between every team segment, even adjacent ones from
        // the same owner (same fill color) -- otherwise two teams owned
        // by the same player would fuse into one solid, unreadable block.
        line: { color: "#000000", width: 1 },
      },
      hovertemplate: `${row.team_name}<br>%{x:.0f} pts<br>$${row.price_paid.toFixed(0)} paid<extra></extra>`,
    }));

    const annotations = players.map((p) => ({
      x: p.total,
      y: p.name,
      text: p.total.toFixed(0),
      showarrow: false,
      xanchor: "left" as const,
      yanchor: "middle" as const,
      xshift: 10,
      font: { size: 12, color: palette.text },
    }));

    return {
      traces,
      categoryArray: players.map((p) => p.name),
      annotations,
      maxTotal: players.length > 0 ? Math.max(...players.map((p) => p.total)) : 1,
    };
  }, [leagueTeamScores, ownerColor, palette.neutral, palette.text]);

  const chartHeight = Math.max(220, leagueChart.categoryArray.length * 56);

  // Top N teams by points gained over their last 7 days of history (not
  // top N by season total -- a team can rank here on a hot week alone).
  // One bar per team, colored by owner for visual consistency with the
  // stacked chart above.
  const weeklyGainChart = useMemo(() => {
    const top = weeklyGains.slice(0, TOP_WEEKLY_GAINERS);
    return {
      teamNames: top.map((r) => r.team_name),
      trace: {
        type: "bar" as const,
        x: top.map((r) => r.team_name),
        y: top.map((r) => r.gain),
        marker: { color: top.map((r) => ownerColor[r.user_id] ?? palette.neutral) },
        hovertemplate: top.map(
          (r) =>
            `${r.team_name} — ${r.display_name}<br>+%{y:.0f} pts over the last ${r.days_tracked} day${
              r.days_tracked === 1 ? "" : "s"
            }<br>${r.latest_score.toFixed(0)} pts total<extra></extra>`
        ),
      },
      maxGain: top.length > 0 ? Math.max(...top.map((r) => r.gain)) : 1,
    };
  }, [weeklyGains, ownerColor, palette.neutral]);

  return (
    <div className="page page-wide">
      <h1>Seasons</h1>

      <label className="season-picker">
        View season
        <select value={selectedSeasonId} onChange={(e) => setSelectedSeasonId(e.target.value)}>
          {seasons.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name} — {STATUS_LABEL[s.status]}
            </option>
          ))}
        </select>
      </label>

      {seasons.length === 0 && <p>No seasons yet.</p>}

      {selectedSeasonId && (
        <div className="season-columns">
          <div>
            <h2>Standings</h2>
            {scoringSummary === null ? (
              <p className="crib-value-note">Loading…</p>
            ) : scoringSummary.owners.length > 0 ? (
              <ScoringSummaryTable scoringSummary={scoringSummary} users={users} />
            ) : (
              <p className="crib-value-note">No scoring data for this season yet.</p>
            )}

            {activeLeagueOptions.length > 0 && (
              <>
                <label className="season-picker">
                  League
                  <select value={selectedLeague} onChange={(e) => setSelectedLeague(e.target.value)}>
                    {activeLeagueOptions.map((lg) => (
                      <option key={lg} value={lg}>
                        {lg}
                      </option>
                    ))}
                  </select>
                </label>

                {leagueChart.categoryArray.length > 0 ? (
                  <div className="season-league-chart">
                    <Plot
                      data={leagueChart.traces}
                      layout={{
                        autosize: true,
                        height: chartHeight,
                        barmode: "stack",
                        showlegend: false,
                        margin: { l: 140, r: 56, t: 8, b: 40 },
                        paper_bgcolor: "transparent",
                        plot_bgcolor: "transparent",
                        font: { size: 12, color: palette.text },
                        xaxis: {
                          title: { text: "Points" },
                          range: [0, leagueChart.maxTotal * 1.15],
                          gridcolor: palette.grid,
                          linecolor: palette.grid,
                          zeroline: false,
                        },
                        yaxis: {
                          categoryorder: "array",
                          categoryarray: leagueChart.categoryArray,
                          gridcolor: palette.grid,
                          linecolor: palette.grid,
                        },
                        annotations: leagueChart.annotations,
                      }}
                      config={{ displayModeBar: false, responsive: true }}
                      style={{ width: "100%", height: chartHeight }}
                      useResizeHandler
                    />
                  </div>
                ) : (
                  <p className="crib-value-note">No teams drafted in {selectedLeague} yet.</p>
                )}

                <h3 className="scoring-summary-heading">Hot This Week</h3>
                {weeklyGainChart.teamNames.length > 0 ? (
                  <div className="season-league-chart">
                    <Plot
                      data={[weeklyGainChart.trace]}
                      layout={{
                        autosize: true,
                        height: 320,
                        showlegend: false,
                        margin: { l: 56, r: 16, t: 8, b: 90 },
                        paper_bgcolor: "transparent",
                        plot_bgcolor: "transparent",
                        font: { size: 12, color: palette.text },
                        xaxis: {
                          categoryorder: "array",
                          categoryarray: weeklyGainChart.teamNames,
                          tickangle: -30,
                          gridcolor: palette.grid,
                          linecolor: palette.grid,
                        },
                        yaxis: {
                          title: { text: "Points gained (last 7 days)" },
                          range: [0, weeklyGainChart.maxGain * 1.15],
                          gridcolor: palette.grid,
                          linecolor: palette.grid,
                          zeroline: false,
                        },
                      }}
                      config={{ displayModeBar: false, responsive: true }}
                      style={{ width: "100%", height: 320 }}
                      useResizeHandler
                    />
                  </div>
                ) : (
                  <p className="crib-value-note">
                    No day-over-day history for {selectedLeague} yet.
                  </p>
                )}
              </>
            )}
          </div>

          <div>
            <h2>Roster</h2>
            <label className="season-picker">
              Player
              <select value={selectedUserId} onChange={(e) => setSelectedUserId(e.target.value)}>
                {users.map((u) => (
                  <option key={u.id} value={u.id}>
                    {u.display_name}
                  </option>
                ))}
              </select>
            </label>
            {selectedUserId && (
              <PlayerRosterPanel seasonId={selectedSeasonId} userId={selectedUserId} />
            )}
          </div>
        </div>
      )}
    </div>
  );
}
