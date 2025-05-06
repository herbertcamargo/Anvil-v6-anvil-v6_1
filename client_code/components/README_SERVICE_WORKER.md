# Service Worker Implementation for Anvil

This document describes the Service Worker implementation for the Anvil application, which provides offline capabilities and improved caching for video processing.

## Overview

Service Workers are a web technology that allows web applications to work offline by intercepting network requests and caching resources. In our implementation, we've added the following features:

1. **Offline Application Support**: Core application files are cached to allow the app to load even without an internet connection.
2. **Video Thumbnail Caching**: Thumbnails of processed videos are cached for faster loading and offline viewing.
3. **WASM Module Caching**: WebAssembly modules used for video processing are cached to improve performance.
4. **Background Sync**: Uploads can be queued when offline and automatically processed when connectivity is restored.
5. **IndexedDB Storage**: Video data and metadata are stored locally for offline access.

## Architecture

The Service Worker implementation consists of the following components:

- `service-worker.js`: The core Service Worker script that handles caching and offline functionality
- `service-worker-registration.js`: Client-side API for registering and interacting with the Service Worker
- `build-service-worker.js`: Build script that prepares and optimizes Service Worker files

### Cache Structure

The implementation uses several cache stores for different purposes:

- `anvil-static-v1`: Static application resources
- `anvil-video-thumbnails-v1`: Video thumbnails
- `anvil-wasm-v1`: WebAssembly modules and related files
- `anvil-dynamic-v1`: Dynamically loaded resources

## Integration with React and Vue Components

The Service Worker functionality is integrated with both React and Vue video processor components. Key integration points include:

- Detecting online/offline status
- Saving videos for offline use
- Generating and caching thumbnails
- Loading videos from offline storage when necessary

## Using the Service Worker API

### Registering the Service Worker

```javascript
import { registerServiceWorker } from '../service-worker-registration';

// Initialize the service worker
registerServiceWorker();
```

### Saving Videos for Offline Use

```javascript
import { storeVideoForOffline } from '../service-worker-registration';

// Save video for offline use
await storeVideoForOffline(videoId, videoArrayBuffer, {
  name: fileName,
  type: mimeType,
  size: fileSize,
  thumbnailUrl: thumbnailUrl,
  timestamp: Date.now()
});
```

### Generating and Caching Thumbnails

```javascript
import { createAndCacheVideoThumbnail } from '../service-worker-registration';

// Create and cache a thumbnail
const thumbnailUrl = await createAndCacheVideoThumbnail(videoId, videoElement);
```

### Loading Offline Videos

```javascript
import { getOfflineVideo } from '../service-worker-registration';

// Get video from offline storage
const { videoData, metadata } = await getOfflineVideo(videoId);
```

## Offline User Experience

When users go offline, they will experience:

1. A notification banner indicating offline status
2. Access to previously saved videos
3. All video processing functionality for saved videos
4. An offline fallback page when attempting to access unavailable content

## Building the Service Worker

The Service Worker files are built and deployed along with the React and Vue components:

```bash
# PowerShell
./build.ps1

# Bash
./build.sh
```

These build scripts:
1. Compile the React and Vue components
2. Minify the Service Worker script
3. Create necessary assets like placeholder thumbnails
4. Generate the offline fallback page

## Browser Compatibility

This Service Worker implementation is compatible with all modern browsers that support:

- Service Worker API
- Cache API
- IndexedDB
- Background Sync API

Internet Explorer and older browsers without Service Worker support will fall back to standard online-only operation.

## Future Enhancements

Potential future enhancements to the Service Worker implementation include:

1. Periodic synchronization of remote content
2. Improved caching strategies for large video files
3. Push notifications for offline events
4. More sophisticated offline analytics
5. Enhanced offline video library management

## Troubleshooting

If you encounter issues with the Service Worker:

1. Check the browser console for error messages
2. Verify the Service Worker is registered correctly
3. Clear the browser's cache and Service Worker registration if needed
4. Ensure the IndexedDB storage isn't full

For more information on Service Workers, refer to the [MDN documentation](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API). 