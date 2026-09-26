import Plotly from "plotly.js-strict-dist-min";
import createPlotlyComponent from "react-plotly.js/factory";

// Single shared Plotly instance/component for the whole app. Needs the
// "strict" bundle, not a smaller partial ("basic", "cartesian") -- per
// plotly.js's own dist/README.md, the barpolar trace (the analytics
// page's radial charts) is only registered in "strict" or the full
// bundle, in neither "basic" nor "cartesian" despite both of those
// mentioning the string "barpolar" in their shared trace-name-suggestion
// code (a real, verified-the-hard-way gotcha -- don't trust a grep match
// on the bundle file as proof a trace type is actually registered;
// check the bundle's documented contents, or render one, instead).
// Built once here so every page reuses the same registered trace types
// instead of each importing (and re-bundling) its own copy.
const Plot = createPlotlyComponent(Plotly);

export default Plot;
