const fs = require('fs-extra');
const path = require('path');

// Paths
const cssDir = path.join(__dirname, '..', 'css');
const themeDir = path.join(__dirname, '..', '..', '..', 'theme', 'css');

// Ensure theme CSS directory exists
fs.ensureDirSync(themeDir);

// Copy all CSS files from the compiled directory to the theme directory
console.log('Copying CSS files to theme directory...');
try {
  const files = fs.readdirSync(cssDir);
  
  files.forEach(file => {
    if (file.endsWith('.css')) {
      const sourcePath = path.join(cssDir, file);
      const targetPath = path.join(themeDir, file);
      
      fs.copyFileSync(sourcePath, targetPath);
      console.log(`Copied: ${file}`);
    }
  });
  
  console.log('All CSS files copied successfully!');
} catch (err) {
  console.error('Error copying CSS files:', err);
  process.exit(1);
} 