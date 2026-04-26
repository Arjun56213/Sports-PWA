// Versioning the cache allows for easy updates when assets change
const CACHE = 'sportvault-cache-v1';
// Static assets to be downloaded and stored for offline access
const ASSETS = [
  '/',
  '/login',
  '/register',
  '/search',
  '/static/css/style.css',
  '/static/js/app.js',
  '/static/icons/batting.png',
  '/static/icons/soccer.png',
  '/static/icons/search.png',
  '/static/manifest.json'
];

// INSTALL EVENT: Pre-caches all essential files during initial app setup
self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting()));
});

// ACTIVATE EVENT: Cleans up old cache versions to manage device storage
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.map((key) => key === CACHE ? null : caches.delete(key)))).then(() => self.clients.claim()) // Takes control of all open tabs immediately
  );
});

// FETCH EVENT: Network-First strategy with Offline Fallback

self.addEventListener('fetch', (event) => {
  // Only intercept GET requests (Data submissions like POST are not cached)
  if (event.request.method !== 'GET') return;
  event.respondWith(
    fetch(event.request).then((response) => {
      // If network is available, clone and update the cache with fresh content
      const copy = response.clone();
      caches.open(CACHE).then((cache) => cache.put(event.request, copy));
      return response;
    }).catch(() => caches.match(event.request).then((cached) => cached || caches.match('/')))
  );
});
