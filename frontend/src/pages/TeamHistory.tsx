import { useEffect, useState } from "react";
import { api, type Team, type TeamHistory as TeamHistoryData } from "../lib/api";

// Test scope: only these leagues are populated with bios/history so far
// (see backend/app/team_history.py) — grouped into separate pickers below
// rather than one giant dropdown. Extend a group's league list (or add a
// new group) as more leagues get covered.
const PICKER_GROUPS: { title: string; leagues: string[] }[] = [
  { title: "EPL", leagues: ["EPL"] },
  { title: "NFL, NBA, NHL", leagues: ["NFL", "NBA", "NHL"] },
];

const CHART_WIDTH = 560;
const CHART_HEIGHT = 220;
const CHART_PADDING = { top: 28, right: 16, bottom: 32, left: 16 };

function SeasonChart({ seasons }: { seasons: TeamHistoryData["seasons"] }) {
  const [hovered, setHovered] = useState<number | null>(null);

  const plotWidth = CHART_WIDTH - CHART_PADDING.left - CHART_PADDING.right;
  const plotHeight = CHART_HEIGHT - CHART_PADDING.top - CHART_PADDING.bottom;
  const maxPoints = Math.max(...seasons.map((s) => s.points), 1);
  const barGap = 18;
  const barWidth = (plotWidth - barGap * (seasons.length - 1)) / seasons.length;

  return (
    <div className="team-history-chart">
      <svg viewBox={`0 0 ${CHART_WIDTH} ${CHART_HEIGHT}`} role="img" aria-label="Fantasy points by season">
        <line
          x1={CHART_PADDING.left}
          y1={CHART_HEIGHT - CHART_PADDING.bottom}
          x2={CHART_WIDTH - CHART_PADDING.right}
          y2={CHART_HEIGHT - CHART_PADDING.bottom}
          className="chart-baseline"
        />
        {seasons.map((s, i) => {
          const barHeight = Math.max((s.points / maxPoints) * plotHeight, 2);
          const x = CHART_PADDING.left + i * (barWidth + barGap);
          const y = CHART_HEIGHT - CHART_PADDING.bottom - barHeight;
          const isHovered = hovered === i;
          return (
            <g
              key={s.season_label}
              onMouseEnter={() => setHovered(i)}
              onMouseLeave={() => setHovered((h) => (h === i ? null : h))}
              className="chart-bar-group"
            >
              {/* full rounded rect, then a flat-bottom patch so only the
                  top corners read as rounded against the baseline */}
              <rect
                x={x}
                y={y}
                width={barWidth}
                height={barHeight}
                rx={4}
                className={isHovered ? "chart-bar hovered" : "chart-bar"}
              />
              <rect
                x={x}
                y={Math.max(y, CHART_HEIGHT - CHART_PADDING.bottom - 4)}
                width={barWidth}
                height={Math.min(4, barHeight)}
                className={isHovered ? "chart-bar hovered" : "chart-bar"}
              />
              <text
                x={x + barWidth / 2}
                y={y - 8}
                textAnchor="middle"
                className="chart-value-label"
              >
                {s.points}
              </text>
              <text
                x={x + barWidth / 2}
                y={CHART_HEIGHT - CHART_PADDING.bottom + 18}
                textAnchor="middle"
                className="chart-axis-label"
              >
                {s.season_label}
              </text>
              <rect
                x={x - barGap / 2}
                y={CHART_PADDING.top}
                width={barWidth + barGap}
                height={plotHeight}
                fill="transparent"
                className="chart-hit-area"
              />
            </g>
          );
        })}
      </svg>
      {hovered !== null && (
        <div className="chart-tooltip" style={{ left: `${((hovered + 0.5) / seasons.length) * 100}%` }}>
          <strong>{seasons[hovered].season_label}</strong>
          <span>{seasons[hovered].points} fantasy points</span>
        </div>
      )}
    </div>
  );
}

// How far the embedded map's viewport extends past the stadium marker on
// each side, in degrees — wide enough to read as "whereabouts in the
// country", not just the immediate neighborhood. Longitude gets a wider
// padding than latitude since degrees of longitude cover less ground the
// further from the equator you are (~0.6x at UK latitudes), and the map
// panel itself is wider than it is tall.
const MAP_LAT_PADDING = 2.8;
const MAP_LON_PADDING = 4.3;

function TeamMap({ name, latitude, longitude }: { name: string; latitude: number; longitude: number }) {
  const bbox = [
    longitude - MAP_LON_PADDING,
    latitude - MAP_LAT_PADDING,
    longitude + MAP_LON_PADDING,
    latitude + MAP_LAT_PADDING,
  ].join(",");
  const src = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&marker=${latitude},${longitude}&layer=mapnik`;
  return (
    <div className="team-history-map">
      <iframe
        title={`Map of where ${name} plays`}
        src={src}
        loading="lazy"
      />
    </div>
  );
}

function TeamHistoryPanel({ teamId }: { teamId: number }) {
  const [history, setHistory] = useState<TeamHistoryData | null>(null);

  useEffect(() => {
    setHistory(null);
    api.get<TeamHistoryData>(`/teams/${teamId}/history`).then(setHistory);
  }, [teamId]);

  if (!history) return <p className="queue-empty">Loading…</p>;

  return (
    <div className="team-history-panel">
      <h2>{history.name}</h2>
      <div className="team-history-header">
        {history.bio ? (
          <p className="team-history-bio">{history.bio}</p>
        ) : (
          <p className="queue-empty">No biography written up for this team yet.</p>
        )}
        {history.latitude != null && history.longitude != null && (
          <TeamMap name={history.name} latitude={history.latitude} longitude={history.longitude} />
        )}
      </div>

      <h3>Fantasy points by season</h3>
      {history.seasons.length === 0 ? (
        <p className="queue-empty">
          No recent seasons to chart — {history.name} hasn't played in the {history.league} within
          the last several years covered so far.
        </p>
      ) : (
        <>
          <SeasonChart seasons={history.seasons} />
          {history.seasons.length < 5 && (
            <p className="team-history-note">
              Showing every season {history.name} has actually played in the {history.league}{" "}
              recently — fewer than 5 because of time spent in a lower division in between.
            </p>
          )}
        </>
      )}
    </div>
  );
}

function TeamPicker({ title, teams }: { title: string; teams: Team[] }) {
  const [selectedTeamId, setSelectedTeamId] = useState<number | null>(null);

  // Grouped by league — a one-league group (EPL) just gets a single
  // optgroup, but this scales cleanly for a group spanning several
  // leagues (NFL/NBA/NHL) without changing the picker's shape.
  const byLeague: Record<string, Team[]> = {};
  for (const t of teams) {
    (byLeague[t.league] ??= []).push(t);
  }
  for (const list of Object.values(byLeague)) {
    list.sort((a, b) => a.name.localeCompare(b.name));
  }
  const leagues = Object.keys(byLeague).sort();

  return (
    <section className="team-history-group">
      <div className="stacked-form" style={{ maxWidth: 320 }}>
        <label>
          {title}
          <select
            value={selectedTeamId ?? ""}
            onChange={(e) => setSelectedTeamId(e.target.value ? Number(e.target.value) : null)}
          >
            <option value="">Choose a team…</option>
            {leagues.map((league) => (
              <optgroup key={league} label={league}>
                {byLeague[league].map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.name}
                  </option>
                ))}
              </optgroup>
            ))}
          </select>
        </label>
      </div>

      {selectedTeamId && (
        <div className="player-picker-panel">
          <TeamHistoryPanel teamId={selectedTeamId} />
        </div>
      )}
    </section>
  );
}

export default function TeamHistory() {
  const [teams, setTeams] = useState<Team[]>([]);

  useEffect(() => {
    api.get<Team[]>("/teams").then(setTeams);
  }, []);

  return (
    <div className="page">
      <h1>Team History</h1>
      <p>
        A short biography and the last several seasons' worth of fantasy points for each team —
        currently a test covering EPL, NFL, NBA, and NHL, ahead of doing the same research pass
        for the other leagues.
      </p>

      {PICKER_GROUPS.map((group) => (
        <TeamPicker
          key={group.title}
          title={group.title}
          teams={teams.filter((t) => group.leagues.includes(t.league))}
        />
      ))}
    </div>
  );
}
