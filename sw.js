const CACHE_NAME = "faraway-zine-full-polish-001-018-v10";
const APP_SHELL = [
  "./", "./index.html", "./archive/", "./about/", "./privacy/", "./preview/",
  "./stories.js", "./assets/site.css", "./assets/site.js",
  "./manifest.webmanifest", "./feed.xml",
  "./icon-192.png", "./icon-512.png", "./favicon-32.png", "./favicon-16.png", "./icon-180.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

// Network-first for same-origin GET requests: readers always see newly
// published articles when online; cached copy is only an offline fallback.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response.ok) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
        }
        return response;
      })
      .catch(() => {
        return caches.match(event.request).then((cached) => {
          if (cached) return cached;
          if (event.request.mode === "navigate") return caches.match("./index.html");
          return Promise.reject(new Error("offline"));
        });
      })
  );
});
