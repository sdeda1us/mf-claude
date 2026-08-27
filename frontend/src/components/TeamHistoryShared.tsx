import { useState } from "react";
import type { TeamHistory as TeamHistoryData } from "../lib/api";

// Shared between the full Team History page (pages/TeamHistory.tsx) and the
// "baseball card" popup (TeamCardModal.tsx) that stands in for it anywhere
// else in the app — both render the same season chart and map, just inside
// different-sized frames.

const CHART_WIDTH = 560;
const CHART_HEIGHT = 220;
const CHART_PADDING = { top: 28, right: 16, bottom: 32, left: 16 };

export function SeasonChart({ seasons }: { seasons: TeamHistoryData["seasons"] }) {
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

export function TeamMap({ name, latitude, longitude }: { name: string; latitude: number; longitude: number }) {
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
