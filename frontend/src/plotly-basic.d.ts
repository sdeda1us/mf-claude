// plotly.js-basic-dist-min ships no types of its own; it's a build of the
// same API surface as plotly.js (just a smaller trace-type bundle, bar
// included), so reuse @types/plotly.js's shape for it.
declare module "plotly.js-basic-dist-min" {
  const Plotly: typeof import("plotly.js");
  export default Plotly;
}
