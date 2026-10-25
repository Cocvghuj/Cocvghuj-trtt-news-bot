const CACHE_NAME='trtt-super-app-v4-787950';
const BASE='/Cocvghuj-trtt-news-bot/';
const urlsToCache=[
  BASE,
  BASE+'index.html',
  BASE+'manifest.json',
  BASE+'tracker.html',
  BASE+'latest_travel_news.html'
];

self.addEventListener('install',e=>{
  e.waitUntil(caches.open(CACHE_NAME).then(c=>c.addAll(urlsToCache).catch(()=>{})));
  self.skipWaiting();
});

self.addEventListener('activate',e=>{
  e.waitUntil(caches.keys().then(keys=>Promise.all(keys.map(k=>{
    if(k!==CACHE_NAME) return caches.delete(k);
  }))));
  self.clients.claim();
});

self.addEventListener('fetch',e=>{
  if(e.request.url.includes('tpo.lv')||e.request.url.includes('amzn.to')||e.request.url.includes('ipapi.co')) return;
  e.respondWith(
    caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{
      if(e.request.method==='GET' && e.request.url.startsWith(self.location.origin)){
        const clone=res.clone();
        caches.open(CACHE_NAME).then(c=>c.put(e.request,clone));
      }
      return res;
    }).catch(()=>caches.match(BASE+'index.html')))
  );
});
