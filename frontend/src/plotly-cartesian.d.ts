// plotly.js-cartesian-dist-min ships no types of its own; it's a build of
// the same API surface as plotly.js (bar/barpolar included, a smaller
// trace-type bundle than the full ~3MB build), so reuse @types/plotly.js's
// shape for it.
declare module "plotly.js-cartesian-dist-min" {
  const Plotly: typeof import("plotly.js");
  export default Plotly;
}
