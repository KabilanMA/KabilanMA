module.exports = {
  content: ["_site/**/*.html", "_site/**/*.js"],
  css: ["_site/assets/css/*.css"],
  output: "_site/assets/css/",
  skippedContentGlobs: ["_site/assets/**/*.html"],
  safelist: {
    // Classes only added at runtime, so they never appear in the built HTML/JS:
    // travel map dot colours (built as `travel-marker-${type}`) and Leaflet's own elements.
    standard: [/^travel-marker/, /^leaflet-/],
  },
};
