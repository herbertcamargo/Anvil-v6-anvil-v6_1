// Service Worker for Anvil Application
// Provides offline capabilities and video thumbnail caching

// Cache names
const STATIC_CACHE = 'anvil-static-v1';
const VIDEO_THUMB_CACHE = 'anvil-video-thumbnails-v1';
const WASM_CACHE = 'anvil-wasm-v1';
const DYNAMIC_CACHE = 'anvil-dynamic-v1';

// Assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/_/theme/css/main.css',
  '/_/theme/wasm/video_processor.js',
  '/_/theme/wasm/video_processor.wasm',
  '/_/theme/wasm/video_processor_wrapper.js',
  '/_/theme/js/react.bundle.js',
  '/_/theme/js/vue.bundle.js'
];

// Install event - cache static assets
self.addEventListener('install', event => {
  console.log('[Service Worker] Installing...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('[Service Worker] Pre-caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('[Service Worker] Installation complete');
        return self.skipWaiting();
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('[Service Worker] Activating...');
  
  const currentCaches = [STATIC_CACHE, VIDEO_THUMB_CACHE, WASM_CACHE, DYNAMIC_CACHE];
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return cacheNames.filter(cacheName => !currentCaches.includes(cacheName));
      })
      .then(cachesToDelete => {
        return Promise.all(cachesToDelete.map(cacheToDelete => {
          console.log('[Service Worker] Deleting old cache:', cacheToDelete);
          return caches.delete(cacheToDelete);
        }));
      })
      .then(() => {
        console.log('[Service Worker] Claiming clients');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve from cache or fetch and cache
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // Handle video thumbnail requests
  if (url.pathname.startsWith('/_/theme/video-thumbnails/')) {
    event.respondWith(handleVideoThumbnail(event.request));
    return;
  }
  
  // Handle WASM files
  if (url.pathname.endsWith('.wasm') || url.pathname.includes('/wasm/')) {
    event.respondWith(handleWasmFile(event.request));
    return;
  }
  
  // Handle all other requests
  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        if (cachedResponse) {
          return cachedResponse;
        }
        
        return fetch(event.request)
          .then(response => {
            // Cache valid responses to dynamic cache
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            const responseToCache = response.clone();
            
            caches.open(DYNAMIC_CACHE)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
            
            return response;
          })
          .catch(error => {
            console.log('[Service Worker] Fetch failed:', error);
            // If we're trying to access an HTML page, return offline page
            if (event.request.headers.get('accept').includes('text/html')) {
              return caches.match('/offline.html');
            }
            
            return new Response('Network error', { status: 503, statusText: 'Service Unavailable' });
          });
      })
  );
});

// Special handling for video thumbnails with enhanced caching
async function handleVideoThumbnail(request) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    // Return cached thumbnail
    return cachedResponse;
  }
  
  try {
    // Fetch and cache the thumbnail
    const response = await fetch(request);
    
    if (!response || response.status !== 200) {
      return response;
    }
    
    const responseToCache = response.clone();
    
    // Store in video thumbnail cache
    const cache = await caches.open(VIDEO_THUMB_CACHE);
    await cache.put(request, responseToCache);
    
    return response;
  } catch (error) {
    console.log('[Service Worker] Video thumbnail fetch failed:', error);
    // Return placeholder image for failed thumbnails
    return caches.match('/assets/placeholder-thumb.jpg');
  }
}

// Special handling for WASM files
async function handleWasmFile(request) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const response = await fetch(request);
    
    if (!response || response.status !== 200) {
      return response;
    }
    
    const responseToCache = response.clone();
    
    // Store in WASM cache
    const cache = await caches.open(WASM_CACHE);
    await cache.put(request, responseToCache);
    
    return response;
  } catch (error) {
    console.log('[Service Worker] WASM fetch failed:', error);
    return new Response('Failed to load WebAssembly module', { status: 503 });
  }
}

// Background sync for deferred uploads when offline
self.addEventListener('sync', event => {
  if (event.tag === 'sync-video-uploads') {
    event.waitUntil(syncVideoUploads());
  }
});

// Function to handle syncing video uploads when coming back online
async function syncVideoUploads() {
  try {
    const db = await openVideoDB();
    const pendingUploads = await db.getAll('pendingUploads');
    
    for (const upload of pendingUploads) {
      try {
        // Attempt to upload the video
        const response = await fetch(upload.url, {
          method: 'POST',
          body: upload.data,
          headers: upload.headers
        });
        
        if (response.ok) {
          // Remove from pending uploads if successful
          await db.delete('pendingUploads', upload.id);
        }
      } catch (error) {
        console.error('[Service Worker] Failed to sync upload:', error);
      }
    }
  } catch (error) {
    console.error('[Service Worker] Sync failed:', error);
  }
}

// IndexedDB for offline data storage
function openVideoDB() {
  return new Promise((resolve, reject) => {
    const dbRequest = indexedDB.open('AnvilVideoDB', 1);
    
    dbRequest.onupgradeneeded = event => {
      const db = event.target.result;
      db.createObjectStore('pendingUploads', { keyPath: 'id' });
      db.createObjectStore('videoMetadata', { keyPath: 'id' });
    };
    
    dbRequest.onsuccess = event => resolve({
      db: event.target.result,
      
      // Helper methods for DB operations
      put: (store, item) => {
        return new Promise((resolve, reject) => {
          const tx = this.db.transaction(store, 'readwrite');
          const req = tx.objectStore(store).put(item);
          req.onsuccess = () => resolve(req.result);
          req.onerror = () => reject(req.error);
        });
      },
      
      getAll: (store) => {
        return new Promise((resolve, reject) => {
          const tx = this.db.transaction(store, 'readonly');
          const req = tx.objectStore(store).getAll();
          req.onsuccess = () => resolve(req.result);
          req.onerror = () => reject(req.error);
        });
      },
      
      delete: (store, key) => {
        return new Promise((resolve, reject) => {
          const tx = this.db.transaction(store, 'readwrite');
          const req = tx.objectStore(store).delete(key);
          req.onsuccess = () => resolve(req.result);
          req.onerror = () => reject(req.error);
        });
      }
    });
    
    dbRequest.onerror = event => reject(event.target.error);
  });
} 