// service-worker.js - LUMINA 787950 - PWA Offline
const CACHE = 'lumina-787950-final-v1';
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(cache => cache.addAll(['./','./index.html','./manifest.json'])));
});
self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
