import { useEffect, useMemo, useState } from "react";
import { api, type AuctionSpending, type AuctionSummary, type RosterEntry } from "../lib/api";
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
  const [rosterEntries, setRosterEntries] = useState<RosterEntry[]>([]);
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

  // Raw per-team sales for the "Where the Money Went" stacked chart --
  // the /spending endpoint only carries per-league averages, not
  // individual sales, so this reuses the roster endpoint the auction
  // room already relies on. Refetches whenever the selected auction (and
  // therefore its season) changes.
  useEffect(() => {
    const season_id = auctions.find((a) => a.id === selectedId)?.season_id;
    if (season_id == null) {
      setRosterEntries([]);
      return;
    }
    api.get<RosterEntry[]>(`/seasons/${season_id}/roster`).then(setRosterEntries);
  }, [selectedId, auctions]);

  // One color + display name per owner, assigned in the same order (and
  // therefore identical to) the radial charts below -- so an owner's
  // color means the same thing in both visuals on this page. "Whole
  // League" is skipped here; it isn't an owner and never appears in the
  // stacked chart.
  const { ownerColor, ownerName, ownerOrder } = useMemo(() => {
    const color: Record<number, string> = {};
    const name: Record<number, string> = {};
    const order: Record<number, number> = {};
    let i = 0;
    for (const facet of spending?.facets ?? []) {
      if (facet.owner_id == null) continue;
      color[facet.owner_id] = palette.owners[i % palette.owners.length];
      name[facet.owner_id] = facet.display_name;
      order[facet.owner_id] = i;
      i++;
    }
    return { ownerColor: color, ownerName: name, ownerOrder: order };
  }, [spending, palette.owners]);

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

  // One bar trace per team sold -- not per owner -- so each is its own
  // visible, hoverable stack segment; every team belonging to the same
  // owner just shares that owner's color. barmode "stack" (below) piles
  // same-x-category traces on top of each other, which only works
  // segment-by-segment across separate traces like this, not from
  // repeated x-values within a single trace. Plotly would otherwise give
  // every one of those traces its own legend entry (one per team), so
  // only the first trace per owner sets showlegend -- the rest share its
  // legendgroup instead, collapsing the legend down to one entry per
  // owner.
  const stackedTraces = useMemo(() => {
    if (!spending) return [];
    const leagues = new Set(spending.leagues);
    const seenOwner = new Set<number>();
    return rosterEntries
      .filter((e) => leagues.has(e.team.league))
      .slice()
      .sort((a, b) => (ownerOrder[a.user_id] ?? 0) - (ownerOrder[b.user_id] ?? 0))
      .map((e) => {
        const name = ownerName[e.user_id] ?? `User #${e.user_id}`;
        const isFirst = !seenOwner.has(e.user_id);
        seenOwner.add(e.user_id);
        return {
          type: "bar" as const,
          x: [e.team.league],
          y: [e.price_paid],
          name,
          legendgroup: String(e.user_id),
          showlegend: isFirst,
          marker: { color: ownerColor[e.user_id] ?? palette.neutral },
          hovertemplate: `${e.team.name} — ${name}<br>$${Number(e.price_paid).toFixed(0)}<extra></extra>`,
        };
      });
  }, [spending, rosterEntries, ownerOrder, ownerColor, ownerName, palette.neutral]);

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
        <>
          <section>
            <h2>Average Team Spend by League</h2>
            <div className="analytics-grid">
              {spending.facets.map((facet) => {
                const color = facet.owner_id == null ? palette.neutral : ownerColor[facet.owner_id];
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
          </section>

          <section>
            <h2>Where the Money Went</h2>
            <div className="analytics-stacked-chart">
              <Plot
                data={stackedTraces}
                layout={{
                  autosize: true,
                  height: 460,
                  barmode: "stack",
                  margin: { l: 56, r: 16, t: 8, b: 40 },
                  paper_bgcolor: "transparent",
                  plot_bgcolor: "transparent",
                  font: { size: 12, color: palette.text },
                  bargap: 0.25,
                  xaxis: {
                    categoryorder: "array",
                    categoryarray: spending.leagues,
                    gridcolor: palette.grid,
                    linecolor: palette.grid,
                  },
                  yaxis: {
                    gridcolor: palette.grid,
                    linecolor: palette.grid,
                    zeroline: false,
                    tickprefix: "$",
                  },
                  legend: {
                    orientation: "h",
                    x: 0,
                    y: 1.12,
                    xanchor: "left",
                    font: { size: 12, color: palette.text },
                  },
                }}
                config={{ displayModeBar: false, responsive: true }}
                style={{ width: "100%", height: 460 }}
                useResizeHandler
              />
            </div>
          </section>
        </>
      )}
    </div>
  );
}
