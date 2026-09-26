// plotly.js-strict-dist-min ships no types of its own; it's a build of the
// same API surface as plotly.js (essentially the full trace-type set,
// barpolar included -- "strict" only strips a few attributes with an XSS
// surface, not any trace modules), so reuse @types/plotly.js's shape for
// it. Needed over the smaller partial bundles ("basic", "cartesian"):
// per plotly.js's own dist/README.md, barpolar/scatterpolar are ONLY
// included in "strict" or the full bundle, not in any smaller partial.
declare module "plotly.js-strict-dist-min" {
  const Plotly: typeof import("plotly.js");
  export default Plotly;
}
