// Service Worker Registration Script
// This script registers the service worker for offline capabilities and better caching

export function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/_/theme/js/service-worker.js')
        .then(registration => {
          console.log('Service Worker registered successfully:', registration.scope);
          
          // Check for updates periodically
          setInterval(() => {
            registration.update();
          }, 60 * 60 * 1000); // Check every hour
        })
        .catch(error => {
          console.error('Service Worker registration failed:', error);
        });
    });
  }
}

// Request permission for notifications
export function requestNotificationPermission() {
  if ('Notification' in window) {
    Notification.requestPermission()
      .then(permission => {
        if (permission === 'granted') {
          console.log('Notification permission granted');
        }
      });
  }
}

// Queue a task for background sync when offline
export function queueBackgroundSync(tag = 'sync-video-uploads') {
  if ('serviceWorker' in navigator && 'SyncManager' in window) {
    navigator.serviceWorker.ready
      .then(registration => {
        return registration.sync.register(tag);
      })
      .then(() => {
        console.log('Background sync registered');
      })
      .catch(error => {
        console.error('Background sync registration failed:', error);
      });
  }
}

// Store video data for offline processing
export function storeVideoForOffline(videoId, videoData, metadata) {
  return new Promise((resolve, reject) => {
    if (!('indexedDB' in window)) {
      reject(new Error('IndexedDB not supported'));
      return;
    }
    
    const request = indexedDB.open('AnvilVideoDB', 1);
    
    request.onerror = event => {
      reject(event.target.error);
    };
    
    request.onupgradeneeded = event => {
      const db = event.target.result;
      
      if (!db.objectStoreNames.contains('videoData')) {
        db.createObjectStore('videoData', { keyPath: 'id' });
      }
      
      if (!db.objectStoreNames.contains('videoMetadata')) {
        db.createObjectStore('videoMetadata', { keyPath: 'id' });
      }
    };
    
    request.onsuccess = event => {
      const db = event.target.result;
      const transaction = db.transaction(['videoData', 'videoMetadata'], 'readwrite');
      
      // Store video data
      const videoStore = transaction.objectStore('videoData');
      videoStore.put({ id: videoId, data: videoData });
      
      // Store metadata
      const metadataStore = transaction.objectStore('videoMetadata');
      metadataStore.put({ id: videoId, ...metadata });
      
      transaction.oncomplete = () => {
        resolve();
      };
      
      transaction.onerror = event => {
        reject(event.target.error);
      };
    };
  });
}

// Get video data from offline storage
export function getOfflineVideo(videoId) {
  return new Promise((resolve, reject) => {
    if (!('indexedDB' in window)) {
      reject(new Error('IndexedDB not supported'));
      return;
    }
    
    const request = indexedDB.open('AnvilVideoDB', 1);
    
    request.onerror = event => {
      reject(event.target.error);
    };
    
    request.onsuccess = event => {
      const db = event.target.result;
      const transaction = db.transaction(['videoData', 'videoMetadata'], 'readonly');
      
      // Get video data
      const videoStore = transaction.objectStore('videoData');
      const videoRequest = videoStore.get(videoId);
      
      // Get metadata
      const metadataStore = transaction.objectStore('videoMetadata');
      const metadataRequest = metadataStore.get(videoId);
      
      let videoData = null;
      let metadata = null;
      
      videoRequest.onsuccess = () => {
        videoData = videoRequest.result ? videoRequest.result.data : null;
        if (metadata !== null) {
          resolve({ videoData, metadata });
        }
      };
      
      metadataRequest.onsuccess = () => {
        metadata = metadataRequest.result;
        if (videoData !== null) {
          resolve({ videoData, metadata });
        }
      };
      
      transaction.onerror = event => {
        reject(event.target.error);
      };
    };
  });
}

// Create and cache video thumbnail
export function createAndCacheVideoThumbnail(videoId, videoElement, time = 1) {
  return new Promise((resolve, reject) => {
    if (!videoElement || !videoElement.videoWidth) {
      reject(new Error('Invalid video element'));
      return;
    }
    
    // If time is specified and valid, set video to that time
    if (time && !isNaN(time) && time >= 0 && time <= videoElement.duration) {
      videoElement.currentTime = time;
    }
    
    // Create a canvas to draw the thumbnail
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    
    // Draw the current frame to the canvas
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to Blob
    canvas.toBlob(blob => {
      if (!blob) {
        reject(new Error('Failed to create thumbnail blob'));
        return;
      }
      
      // Create a URL for the blob
      const thumbnailUrl = URL.createObjectURL(blob);
      
      // Cache the thumbnail in the service worker cache
      if ('caches' in window) {
        const cacheName = 'anvil-video-thumbnails-v1';
        const thumbnailPath = `/_/theme/video-thumbnails/${videoId}.jpg`;
        
        caches.open(cacheName)
          .then(cache => {
            // Create a response to cache
            const response = new Response(blob, {
              headers: {
                'Content-Type': 'image/jpeg',
                'Cache-Control': 'max-age=86400'
              }
            });
            
            // Add the thumbnail to the cache
            return cache.put(thumbnailPath, response);
          })
          .then(() => {
            resolve(thumbnailUrl);
          })
          .catch(error => {
            console.error('Failed to cache thumbnail:', error);
            resolve(thumbnailUrl); // Still resolve with the URL even if caching fails
          });
      } else {
        resolve(thumbnailUrl);
      }
    }, 'image/jpeg', 0.8);
  });
}

// Check if a video is available offline
export function isVideoAvailableOffline(videoId) {
  return new Promise((resolve, reject) => {
    if (!('indexedDB' in window)) {
      resolve(false);
      return;
    }
    
    const request = indexedDB.open('AnvilVideoDB', 1);
    
    request.onerror = () => {
      resolve(false);
    };
    
    request.onsuccess = event => {
      const db = event.target.result;
      
      if (!db.objectStoreNames.contains('videoData')) {
        resolve(false);
        return;
      }
      
      const transaction = db.transaction(['videoData'], 'readonly');
      const store = transaction.objectStore('videoData');
      const getRequest = store.get(videoId);
      
      getRequest.onsuccess = () => {
        resolve(!!getRequest.result);
      };
      
      getRequest.onerror = () => {
        resolve(false);
      };
    };
  });
} 