import { useEffect, useState } from "react";

// Reads the shared chart palette from CSS custom properties so it stays
// in sync with light/dark mode -- Plotly renders into its own SVG and
// won't pick up var(--x) the way regular CSS does, so the concrete color
// has to be resolved in JS. --chart-* variables are a categorical
// palette distinct from the site's UI accents (--sky, --grass, etc.) --
// see index.css's :root for why (bumped saturation, validated with
// dataviz's validate_palette.js). Shared by every page with a Plotly
// chart (Analytics, Seasons) so an owner's color means the same thing
// wherever it appears.
export function readChartPalette() {
  const style = getComputedStyle(document.documentElement);
  const read = (name: string, fallback: string) => style.getPropertyValue(name).trim() || fallback;
  return {
    // A non-owner series (e.g. "Whole League") gets a neutral ink tone
    // rather than competing for one of the six owner hues.
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

export function useChartPalette() {
  const [palette, setPalette] = useState(readChartPalette);
  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const update = () => setPalette(readChartPalette());
    mq.addEventListener("change", update);
    return () => mq.removeEventListener("change", update);
  }, []);
  return palette;
}
