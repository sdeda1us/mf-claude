import { useEffect, useMemo, useState } from "react";
import {
  api,
  type AuctionSpending,
  type AuctionSummary,
  type LeagueRules,
  type RosterEntry,
  type Team,
} from "../lib/api";
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

// True on narrow (roughly phone-width) viewports. Used to flip the
// "Where the Money Went" stacked chart to horizontal bars there -- with
// 9-11 league categories, a vertical layout leaves so little width per
// bar on a phone that Plotly auto-rotates the labels diagonally (exactly
// the "please don't make me read at an angle" mistake the rest of this
// page's styling deliberately avoids). Horizontal bars sidestep it
// entirely, the same fix already used for "Still on the Board".
function useIsNarrow(breakpointPx: number): boolean {
  const [isNarrow, setIsNarrow] = useState(
    () => window.matchMedia(`(max-width: ${breakpointPx}px)`).matches
  );
  useEffect(() => {
    const mq = window.matchMedia(`(max-width: ${breakpointPx}px)`);
    const update = () => setIsNarrow(mq.matches);
    mq.addEventListener("change", update);
    return () => mq.removeEventListener("change", update);
  }, [breakpointPx]);
  return isNarrow;
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
  const [teams, setTeams] = useState<Team[]>([]);
  const [rules, setRules] = useState<LeagueRules | null>(null);
  const [loading, setLoading] = useState(false);
  const palette = useAnalyticsPalette();
  const stackedChartNarrow = useIsNarrow(700);

  // Static reference data for the "Still on the Board" chart -- the full
  // team catalog (to find what's unsold) and roster limits (to know how
  // many slots exist per league in the first place). Same endpoints the
  // auction room already uses; neither depends on which auction is
  // selected.
  useEffect(() => {
    api.get<Team[]>("/teams").then(setTeams);
    api.get<LeagueRules>("/leagues/rules").then(setRules);
  }, []);

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
          orientation: stackedChartNarrow ? ("h" as const) : ("v" as const),
          x: stackedChartNarrow ? [e.price_paid] : [e.team.league],
          y: stackedChartNarrow ? [e.team.league] : [e.price_paid],
          name,
          legendgroup: String(e.user_id),
          showlegend: isFirst,
          marker: {
            color: ownerColor[e.user_id] ?? palette.neutral,
            // A hairline between every team segment, even adjacent ones
            // from the same owner (same fill color) -- otherwise two
            // teams bought by the same person in the same league would
            // fuse into one solid block with no visible seam.
            line: { color: "#000000", width: 1 },
          },
          hovertemplate: `${e.team.name} — ${name}<br>$${Number(e.price_paid).toFixed(0)}<extra></extra>`,
        };
      });
  }, [spending, rosterEntries, ownerOrder, ownerColor, ownerName, palette.neutral, stackedChartNarrow]);

  // Actual price paid vs. Team.default_value (the league-wide modeled
  // valuation shown everywhere else in the app, e.g. the team board's
  // "Your Value" column before an owner overrides it) -- deliberately
  // NOT each owner's own private crib sheet override, since every
  // crib-sheet endpoint today is scoped so nobody but the owner
  // themselves can ever see it; default_value is the one valuation this
  // shared page can show without leaking anyone's private numbers.
  // One trace per owner (not per team, unlike the stacked chart above) --
  // each point is already independently positioned by its own x/y, so
  // there's no same-color-adjacent-segment ambiguity that needs the
  // legendgroup trick this time, and Plotly's default one-entry-per-trace
  // legend is exactly what's wanted: one entry per owner.
  const valueVsPriceChart = useMemo(() => {
    if (!spending) return { traces: [], maxVal: 1 };
    const leagues = new Set(spending.leagues);
    const priced = rosterEntries.filter(
      (e) => leagues.has(e.team.league) && e.team.default_value != null
    );
    const byOwner = new Map<number, { x: number[]; y: number[]; text: string[] }>();
    for (const e of priced) {
      const bucket = byOwner.get(e.user_id) ?? { x: [], y: [], text: [] };
      bucket.x.push(e.team.default_value as number);
      bucket.y.push(e.price_paid);
      bucket.text.push(e.team.name);
      byOwner.set(e.user_id, bucket);
    }
    const maxVal =
      priced.length === 0
        ? 1
        : Math.max(...priced.flatMap((e) => [e.team.default_value as number, e.price_paid])) * 1.1;

    const referenceLine = {
      type: "scatter" as const,
      mode: "lines" as const,
      x: [0, maxVal],
      y: [0, maxVal],
      line: { color: palette.grid, width: 1.5, dash: "dash" as const },
      hoverinfo: "skip" as const,
      showlegend: false,
    };
    const ownerTraces = Array.from(byOwner.entries())
      .sort(([a], [b]) => (ownerOrder[a] ?? 0) - (ownerOrder[b] ?? 0))
      .map(([uid, bucket]) => ({
        type: "scatter" as const,
        mode: "markers" as const,
        x: bucket.x,
        y: bucket.y,
        text: bucket.text,
        name: ownerName[uid] ?? `User #${uid}`,
        marker: {
          color: ownerColor[uid] ?? palette.neutral,
          size: 10,
          line: { color: "#000000", width: 1 },
        },
        hovertemplate: "%{text}<br>Predicted: $%{x:.0f}<br>Paid: $%{y:.0f}<extra></extra>",
      }));
    return { traces: [referenceLine, ...ownerTraces], maxVal };
  }, [spending, rosterEntries, ownerOrder, ownerColor, ownerName, palette.grid, palette.neutral]);

  // "Still on the Board": how many roster slots are left in each league
  // (roster_limits × number of owners, minus how many have already sold
  // this session) and, on hover, which unsold teams are the most
  // valuable by the same modeled default_value used in the scatter chart
  // above -- i.e. what's still worth grabbing. A league whose owner
  // count can't be read yet (spending not loaded) or whose rules/teams
  // haven't loaded returns nothing rather than a misleading partial bar.
  const openingsChart = useMemo(() => {
    if (!spending || !rules) return { leagues: [], slotsRemaining: [], hovertext: [] };
    const numOwners = spending.facets.filter((f) => f.owner_id != null).length;
    const soldIds = new Set(rosterEntries.map((e) => e.team.id));
    const slotsRemaining: number[] = [];
    const hovertext: string[] = [];
    for (const lg of spending.leagues) {
      const limit = rules.roster_limits[lg] ?? 0;
      const soldCount = rosterEntries.filter((e) => e.team.league === lg).length;
      const remaining = Math.max(0, limit * numOwners - soldCount);
      slotsRemaining.push(remaining);

      const topAvailable = teams
        .filter((t) => t.league === lg && !soldIds.has(t.id) && t.default_value != null)
        .sort((a, b) => (b.default_value as number) - (a.default_value as number))
        .slice(0, 3);
      const lines = [`${lg}: ${remaining} slot${remaining === 1 ? "" : "s"} open`];
      if (topAvailable.length > 0) {
        lines.push(...topAvailable.map((t, i) => `${i + 1}. ${t.name} — $${t.default_value}`));
      } else {
        lines.push("No unsold teams with a modeled value");
      }
      hovertext.push(lines.join("<br>"));
    }
    return { leagues: spending.leagues, slotsRemaining, hovertext };
  }, [spending, rules, rosterEntries, teams]);

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
                  margin: stackedChartNarrow
                    ? { l: 72, r: 16, t: 8, b: 40 }
                    : { l: 56, r: 16, t: 8, b: 40 },
                  paper_bgcolor: "transparent",
                  plot_bgcolor: "transparent",
                  font: { size: 12, color: palette.text },
                  bargap: 0.25,
                  // Same category axis, different position -- narrow
                  // viewports flip to horizontal bars (see stackedTraces),
                  // so the league labels land on y instead of x, sidestepping
                  // the "not enough width per category" diagonal-label
                  // problem entirely rather than fighting it with tickangle.
                  xaxis: stackedChartNarrow
                    ? { gridcolor: palette.grid, linecolor: palette.grid, zeroline: false, tickprefix: "$" }
                    : {
                        categoryorder: "array",
                        categoryarray: spending.leagues,
                        gridcolor: palette.grid,
                        linecolor: palette.grid,
                      },
                  yaxis: stackedChartNarrow
                    ? {
                        categoryorder: "array",
                        categoryarray: spending.leagues,
                        autorange: "reversed",
                        gridcolor: palette.grid,
                        linecolor: palette.grid,
                      }
                    : { gridcolor: palette.grid, linecolor: palette.grid, zeroline: false, tickprefix: "$" },
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

          <section>
            <div className="analytics-two-col">
              <div>
                <h2>Price Paid vs. Predicted Value</h2>
                <div className="analytics-scatter-chart">
                  <Plot
                    data={valueVsPriceChart.traces}
                    layout={{
                      autosize: true,
                      height: 460,
                      margin: { l: 60, r: 16, t: 8, b: 48 },
                      paper_bgcolor: "transparent",
                      plot_bgcolor: "transparent",
                      font: { size: 12, color: palette.text },
                      xaxis: {
                        title: { text: "Predicted value ($)" },
                        range: [0, valueVsPriceChart.maxVal],
                        tickprefix: "$",
                        gridcolor: palette.grid,
                        linecolor: palette.grid,
                        zeroline: false,
                        // Without this, satisfying yaxis's 1:1 scaleanchor
                        // below stretches THIS axis's range to fill the
                        // container's actual (wide, not square) pixel
                        // dimensions instead -- "domain" tells Plotly to pad
                        // the plot area with whitespace instead, keeping the
                        // range exactly [0, maxVal] as set here.
                        constrain: "domain",
                      },
                      yaxis: {
                        title: { text: "Actual price paid ($)" },
                        range: [0, valueVsPriceChart.maxVal],
                        tickprefix: "$",
                        gridcolor: palette.grid,
                        linecolor: palette.grid,
                        zeroline: false,
                        // Locks a true 1:1 aspect ratio to the x-axis, so the
                        // dashed reference line always reads as an honest 45°
                        // diagonal (points above it overpaid relative to the
                        // model, below it underpaid) regardless of the
                        // container's own width/height.
                        scaleanchor: "x",
                        scaleratio: 1,
                        constrain: "domain",
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
              </div>

              <div>
                <h2>Still on the Board</h2>
                <p className="analytics-facet-meta">
                  Open roster slots per league, plus the highest-valued unsold teams on hover
                </p>
                <div className="analytics-openings-chart">
                  <Plot
                    data={[
                      {
                        type: "bar",
                        orientation: "h",
                        y: openingsChart.leagues,
                        x: openingsChart.slotsRemaining,
                        hovertext: openingsChart.hovertext,
                        hovertemplate: "%{hovertext}<extra></extra>",
                        marker: { color: palette.neutral },
                      },
                    ]}
                    layout={{
                      autosize: true,
                      height: 460,
                      margin: { l: 56, r: 16, t: 8, b: 40 },
                      paper_bgcolor: "transparent",
                      plot_bgcolor: "transparent",
                      font: { size: 12, color: palette.text },
                      xaxis: {
                        title: { text: "Open roster slots" },
                        gridcolor: palette.grid,
                        linecolor: palette.grid,
                        zeroline: false,
                      },
                      yaxis: {
                        categoryorder: "array",
                        categoryarray: openingsChart.leagues,
                        autorange: "reversed",
                        gridcolor: palette.grid,
                        linecolor: palette.grid,
                      },
                    }}
                    config={{ displayModeBar: false, responsive: true }}
                    style={{ width: "100%", height: 460 }}
                    useResizeHandler
                  />
                </div>
              </div>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
