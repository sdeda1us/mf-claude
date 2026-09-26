import { useEffect, useMemo, useState } from "react";
import { api, type AuctionSpending, type AuctionSummary } from "../lib/api";
import Plot from "../lib/plotly";

// Reads the analytics chart palette from CSS custom properties so it stays
// in sync with light/dark mode -- Plotly renders into its own SVG and
// won't pick up var(--x) the way regular CSS does, so the concrete color
// has to be resolved in JS (same approach as the auction page's teams-sold
// chart). --chart-* variables are a categorical palette distinct from the
// site's UI accents (--sky, --grass, etc.) -- see index.css's :root for
// why (bumped saturation, validated with dataviz's validate_palette.js).
function readAnalyticsPalette() {
  const style = getComputedStyle(document.documentElement);
  const read = (name: string, fallback: string) => style.getPropertyValue(name).trim() || fallback;
  return {
    // "Whole League" isn't a person, so it gets a neutral ink tone rather
    // than competing for one of the six owner hues.
    neutral: read("--ink-soft", "#58513f"),
    owners: [
      read("--chart-red", "#c8372e"),
      read("--chart-sky", "#2f7ba8"),
      read("--chart-gold", "#d9a73b"),
      read("--chart-teal", "#0d9488"),
      read("--chart-violet", "#7a5ea8"),
      read("--chart-grass", "#1f8a4a"),
    ],
    grid: read("--rule", "#e0d3ab"),
    text: read("--ink-soft", "#58513f"),
  };
}

function useAnalyticsPalette() {
  const [palette, setPalette] = useState(readAnalyticsPalette);
  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const update = () => setPalette(readAnalyticsPalette());
    mq.addEventListener("change", update);
    return () => mq.removeEventListener("change", update);
  }, []);
  return palette;
}

function auctionLabel(a: AuctionSummary): string {
  const sessionLabel = a.session === "fall" ? "Fall" : "Spring";
  const statusLabel =
    a.status === "complete" ? "complete" : a.status === "live" ? "in progress" : "not started";
  return `${a.season_name} — ${sessionLabel} (${statusLabel})`;
}

export default function Analytics() {
  const [auctions, setAuctions] = useState<AuctionSummary[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [spending, setSpending] = useState<AuctionSpending | null>(null);
  const [loading, setLoading] = useState(false);
  const palette = useAnalyticsPalette();

  useEffect(() => {
    api.get<AuctionSummary[]>("/analytics/auctions").then((rows) => {
      setAuctions(rows);
      // The backend already orders these in-progress-first, then
      // most-recently-created first, so the first row here is exactly
      // "the most recent auction, counting one in progress as most
      // recent" -- the default this page should land on.
      if (rows.length > 0) setSelectedId(rows[0].id);
    });
  }, []);

  useEffect(() => {
    if (selectedId == null) return;
    setLoading(true);
    api
      .get<AuctionSpending>(`/analytics/auctions/${selectedId}/spending`)
      .then(setSpending)
      .finally(() => setLoading(false));
  }, [selectedId]);

  // Every facet's radial axis shares this same upper bound, so a glance
  // across the grid compares like for like -- without it, an owner who's
  // spent less would draw a bar out to the same radius as the big
  // spenders, since each chart would otherwise auto-scale to its own max.
  const maxR = useMemo(() => {
    if (!spending) return 1;
    let max = 0;
    for (const facet of spending.facets) {
      for (const v of Object.values(facet.by_league)) {
        if (v > max) max = v;
      }
    }
    return max > 0 ? max * 1.1 : 1;
  }, [spending]);

  return (
    <div className="page page-wide">
      <h1>Auction Analytics</h1>

      <div className="analytics-picker">
        <label>
          Viewing
          <select
            value={selectedId ?? ""}
            onChange={(e) => setSelectedId(Number(e.target.value))}
          >
            {auctions.map((a) => (
              <option key={a.id} value={a.id}>
                {auctionLabel(a)}
              </option>
            ))}
          </select>
        </label>
      </div>

      {!spending ? (
        <p>{loading ? "Loading…" : auctions.length === 0 ? "No auctions yet." : ""}</p>
      ) : (
        <div className="analytics-grid">
          {spending.facets.map((facet, i) => {
            const color =
              facet.owner_id == null
                ? palette.neutral
                : palette.owners[(i - 1) % palette.owners.length];
            return (
              <div key={facet.owner_id ?? "league"} className="analytics-facet">
                <h3 className="analytics-facet-title">{facet.display_name}</h3>
                <p className="analytics-facet-meta">
                  {facet.teams_sold} team{facet.teams_sold === 1 ? "" : "s"} sold
                </p>
                <div className="analytics-facet-chart">
                  <Plot
                    data={[
                      {
                        type: "barpolar",
                        theta: spending.leagues,
                        r: spending.leagues.map((lg) => facet.by_league[lg] ?? 0),
                        marker: { color },
                        hovertemplate: "%{theta}: $%{r:.0f} avg/team<extra></extra>",
                      },
                    ]}
                    layout={{
                      width: 260,
                      height: 260,
                      margin: { l: 24, r: 24, t: 24, b: 24 },
                      paper_bgcolor: "transparent",
                      font: { size: 10, color: palette.text },
                      polar: {
                        bgcolor: "transparent",
                        radialaxis: {
                          range: [0, maxR],
                          showticklabels: true,
                          tickfont: { size: 8, color: palette.text },
                          gridcolor: palette.grid,
                          linecolor: palette.grid,
                          nticks: 3,
                          tickprefix: "$",
                        },
                        angularaxis: {
                          gridcolor: palette.grid,
                          linecolor: palette.grid,
                          tickfont: { size: 9, color: palette.text },
                        },
                      },
                    }}
                    config={{ displayModeBar: false, responsive: false }}
                    style={{ width: 260, height: 260 }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
