import Plotly from "plotly.js-cartesian-dist-min";
import createPlotlyComponent from "react-plotly.js/factory";

// Single shared Plotly instance/component for the whole app — the
// "cartesian" partial bundle (bar + barpolar + more, still well short of
// the full ~3MB build) rather than "basic", since the analytics page's
// radial charts need the barpolar trace type that "basic" doesn't
// register. Built once here so every page reuses the same registered
// trace types instead of each importing (and re-bundling) its own copy.
const Plot = createPlotlyComponent(Plotly);

export default Plot;
