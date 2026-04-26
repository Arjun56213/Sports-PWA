// Verification of browser compatibility for Progressive Web App features
if ('serviceWorker' in navigator) {
  // Event listener ensures registration occurs only after the main page assets load
  window.addEventListener('load', () => {
    // Register the background script responsible for caching and offline support
    navigator.serviceWorker.register('/static/js/serviceworker.js').catch(() => {});
    /* Error handling for failed registration in restricted environments */
  });
}
