const fs = require('fs-extra');
const path = require('path');
const uglifyJS = require('uglify-js');

console.log('Building and deploying Service Worker files...');

// Paths
const srcDir = path.join(__dirname, '..', 'src');
const themeDir = path.join(__dirname, '..', '..', '..', 'theme');
const themeJsDir = path.join(themeDir, 'js');
const placeholderDir = path.join(themeDir, 'assets');

// Create directories if they don't exist
fs.ensureDirSync(themeJsDir);
fs.ensureDirSync(placeholderDir);
fs.ensureDirSync(path.join(themeDir, 'video-thumbnails'));

// Copy and minify the service worker
try {
  // Read service worker source
  const swSource = fs.readFileSync(path.join(srcDir, 'service-worker.js'), 'utf8');
  
  // Minify the service worker code
  const minifiedSW = uglifyJS.minify(swSource);
  
  if (minifiedSW.error) {
    throw new Error(`Error minifying service worker: ${minifiedSW.error}`);
  }
  
  // Write the minified service worker to the theme directory
  fs.writeFileSync(path.join(themeJsDir, 'service-worker.js'), minifiedSW.code);
  console.log('Service Worker minified and copied to theme directory');
} catch (err) {
  console.error('Error processing service worker:', err);
  process.exit(1);
}

// Create a placeholder thumbnail image for offline use
try {
  const placeholderExists = fs.existsSync(path.join(placeholderDir, 'placeholder-thumb.jpg'));
  
  if (!placeholderExists) {
    // Create a simple placeholder image using node-canvas (if available)
    try {
      const { createCanvas } = require('canvas');
      const canvas = createCanvas(320, 180);
      const ctx = canvas.getContext('2d');
      
      // Fill with dark gray
      ctx.fillStyle = '#333';
      ctx.fillRect(0, 0, 320, 180);
      
      // Add text
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 24px Arial';
      ctx.textAlign = 'center';
      ctx.fillText('Offline', 160, 90);
      
      // Save as JPEG
      const buffer = canvas.toBuffer('image/jpeg');
      fs.writeFileSync(path.join(placeholderDir, 'placeholder-thumb.jpg'), buffer);
      console.log('Placeholder thumbnail created');
    } catch (canvasErr) {
      // If canvas is not available, copy a placeholder from assets (if it exists)
      const defaultPlaceholder = path.join(__dirname, 'assets', 'placeholder-thumb.jpg');
      if (fs.existsSync(defaultPlaceholder)) {
        fs.copyFileSync(defaultPlaceholder, path.join(placeholderDir, 'placeholder-thumb.jpg'));
        console.log('Default placeholder thumbnail copied');
      } else {
        console.warn('Could not create placeholder thumbnail. Using an empty file.');
        // Create an empty file as placeholder
        fs.writeFileSync(path.join(placeholderDir, 'placeholder-thumb.jpg'), '');
      }
    }
  }
} catch (err) {
  console.error('Error creating placeholder thumbnail:', err);
}

// Create a simple offline.html page
try {
  const offlinePage = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Offline - Anvil App</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      padding: 20px;
      text-align: center;
      background-color: #f8f9fa;
      color: #333;
    }
    h1 {
      color: #4CAF50;
    }
    .icon {
      font-size: 64px;
      margin-bottom: 20px;
    }
    .card {
      background-color: white;
      border-radius: 8px;
      padding: 30px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      max-width: 500px;
      width: 100%;
    }
    .btn {
      display: inline-block;
      background-color: #4CAF50;
      color: white;
      padding: 10px 20px;
      border-radius: 4px;
      text-decoration: none;
      margin-top: 20px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="icon">📵</div>
    <h1>You're Offline</h1>
    <p>It looks like you lost your internet connection. Some features may be unavailable until you're back online.</p>
    <p>Don't worry - any videos you've previously viewed should still be available in offline mode.</p>
    <a href="/" class="btn">Try Again</a>
  </div>
  <script>
    // Check if we're back online
    window.addEventListener('online', () => {
      window.location.reload();
    });
    
    // Check for cached content
    if ('caches' in window) {
      document.addEventListener('DOMContentLoaded', () => {
        caches.open('anvil-static-v1').then(cache => {
          cache.keys().then(keys => {
            const hasCache = keys.length > 0;
            if (hasCache) {
              document.querySelector('.btn').style.display = 'inline-block';
            } else {
              document.querySelector('.btn').style.display = 'none';
            }
          });
        });
      });
    }
  </script>
</body>
</html>
  `.trim();
  
  fs.writeFileSync(path.join(themeDir, 'offline.html'), offlinePage);
  console.log('Offline page created');
} catch (err) {
  console.error('Error creating offline page:', err);
}

console.log('Service Worker build complete!'); 