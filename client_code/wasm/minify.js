const fs = require('fs');
const path = require('path');
const UglifyJS = require('uglify-js');

// Paths
const wrapperPath = path.join(__dirname, 'src', 'video_processor_wrapper.js');
const outputDir = path.join(__dirname, '..', '..', 'theme', 'wasm');

// Read the wrapper file
console.log('Reading JavaScript wrapper file...');
const wrapperCode = fs.readFileSync(wrapperPath, 'utf8');

// Minify the code
console.log('Minifying JavaScript code...');
const result = UglifyJS.minify(wrapperCode, {
  compress: true,
  mangle: true
});

if (result.error) {
  console.error('Error minifying code:', result.error);
  process.exit(1);
}

// Ensure the output directory exists
if (!fs.existsSync(outputDir)) {
  console.log('Creating output directory...');
  fs.mkdirSync(outputDir, { recursive: true });
}

// Write the minified code to the output file
const outputPath = path.join(outputDir, 'video_processor_wrapper.min.js');
console.log(`Writing minified code to ${outputPath}...`);
fs.writeFileSync(outputPath, result.code);

// Also copy the original unminified file for debugging
const debugOutputPath = path.join(outputDir, 'video_processor_wrapper.js');
console.log(`Copying unminified code to ${debugOutputPath} for debugging...`);
fs.copyFileSync(wrapperPath, debugOutputPath);

console.log('JavaScript minification complete!'); 