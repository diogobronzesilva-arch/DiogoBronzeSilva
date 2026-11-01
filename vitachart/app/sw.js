/* The production build supplies the complete, versioned application shell. */
const CACHE_NAME = "vitachart-app-927c8dfb1c572fd7";
const PRECACHE_URLS = ["/vitachart/app/assets/cormorant-garamond-latin-300-normal-BuXLI6C0.woff","/vitachart/app/assets/cormorant-garamond-latin-300-normal-Cw-E_7L1.woff2","/vitachart/app/assets/cormorant-garamond-latin-400-normal-B-1hWBU7.woff2","/vitachart/app/assets/cormorant-garamond-latin-400-normal-B7YtguxJ.woff","/vitachart/app/assets/cormorant-garamond-latin-500-normal-BsRWmXhO.woff2","/vitachart/app/assets/cormorant-garamond-latin-500-normal-zIXX3Q-H.woff","/vitachart/app/assets/cormorant-garamond-latin-600-normal-2CBVLo0M.woff","/vitachart/app/assets/cormorant-garamond-latin-600-normal-Co1r35X9.woff2","/vitachart/app/assets/cormorant-garamond-latin-700-normal-DajfzrDU.woff2","/vitachart/app/assets/cormorant-garamond-latin-700-normal-O25Qpphb.woff","/vitachart/app/assets/i18n-messages-CEzyzqPp.js","/vitachart/app/assets/index-BmNIGttu.js","/vitachart/app/assets/index-BmmaaGaq.js","/vitachart/app/assets/index-CrgVEOc_.css","/vitachart/app/assets/index-Fr_WOfWC.js","/vitachart/app/assets/input-switch-polyfill-BJDq8-B4.css","/vitachart/app/assets/input-switch-polyfill-DRG0cyTV.js","/vitachart/app/assets/plus-jakarta-sans-latin-200-normal-Cl6o9Wxk.woff","/vitachart/app/assets/plus-jakarta-sans-latin-200-normal-CzYjBVy3.woff2","/vitachart/app/assets/plus-jakarta-sans-latin-300-normal-n-kmFdAV.woff","/vitachart/app/assets/plus-jakarta-sans-latin-300-normal-ubitlNZx.woff2","/vitachart/app/assets/plus-jakarta-sans-latin-400-normal-BDKaGhyp.woff","/vitachart/app/assets/plus-jakarta-sans-latin-400-normal-Dhut76fR.woff2","/vitachart/app/assets/plus-jakarta-sans-latin-500-normal-Bf-nb4oT.woff2","/vitachart/app/assets/plus-jakarta-sans-latin-500-normal-DYtqi0QS.woff","/vitachart/app/assets/plus-jakarta-sans-latin-600-normal-BR_Ojra4.woff","/vitachart/app/assets/plus-jakarta-sans-latin-600-normal-DLTa1BUW.woff2","/vitachart/app/assets/plus-jakarta-sans-latin-700-normal-CfpNZvy6.woff2","/vitachart/app/assets/plus-jakarta-sans-latin-700-normal-DqEcQeE5.woff","/vitachart/app/assets/plus-jakarta-sans-latin-800-normal-BRNHt2w0.woff","/vitachart/app/assets/plus-jakarta-sans-latin-800-normal-CusIZhrK.woff2","/vitachart/app/assets/vendor-icons-OUxamrC9.js","/vitachart/app/assets/vendor-react-o5BqKlwb.js","/vitachart/app/assets/vendor-temporal-D0rLQFhn.js","/vitachart/app/assets/web-C9ZXgfB6.js","/vitachart/app/assets/web-D3NibUxE.js","/vitachart/app/assets/web-Ds1W6Dm5.js","/vitachart/app/icon.svg","/vitachart/app/icons/apple-touch-icon.png","/vitachart/app/icons/icon-192.png","/vitachart/app/icons/icon-512.png","/vitachart/app/icons/maskable-512.png","/vitachart/app/index.html","/vitachart/app/manifest.webmanifest","/vitachart/app/privacy-en.html","/vitachart/app/privacy-es.html","/vitachart/app/privacy-fr.html","/vitachart/app/privacy.html","/vitachart/app/release-info.json"];
const STATIC_PATHS = new Set(PRECACHE_URLS);

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(
    PRECACHE_URLS.map((url) => new Request(url, { cache: 'reload' }))
  )));
  // Updates wait until all existing windows close, preserving in-progress edits.
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((key) => key !== CACHE_NAME && (
      key.startsWith('vitachart-app-') || key === 'vitachart-cache-v2'
    )).map((key) => caches.delete(key)));
    await self.clients.claim();
  })());
});

self.addEventListener('message', (event) => {
  if (event.data?.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  if (event.data?.type === 'VITACHART_OFFLINE_STATUS') {
    event.waitUntil((async () => {
      const cache = await caches.open(CACHE_NAME);
      const entries = new Set((await cache.keys()).map((request) => new URL(request.url).pathname));
      const ready = PRECACHE_URLS.every((url) => entries.has(url));
      event.ports[0]?.postMessage({ type: ready ? 'VITACHART_OFFLINE_READY' : 'VITACHART_OFFLINE_UNAVAILABLE', version: CACHE_NAME });
    })());
  }
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;

  // All query variants open the same shell; the URL (and demo isolation) stays intact.
  const shellUrl = PRECACHE_URLS.find((p) => p.endsWith('/index.html') || p === '/index.html') || '/index.html';
  const shellDir = shellUrl.replace(/index\.html$/, '');
  const isShell = request.mode === 'navigate' && (
    url.pathname === '/' ||
    url.pathname === '/index.html' ||
    url.pathname === shellUrl ||
    url.pathname === shellDir ||
    url.pathname === shellDir.replace(/\/$/, '')
  );
  if (!isShell && (!STATIC_PATHS.has(url.pathname) || url.search)) return;

  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    return await cache.match(isShell ? shellUrl : url.pathname) || fetch(request);
  })());
});
