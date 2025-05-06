# This script builds the WebAssembly module for video processing
# Note: You need to have Emscripten SDK installed and activated in your environment

# Message for users
Write-Host "Building WebAssembly module for video processing..."

# Check if Node.js is available for JavaScript processing
$node = Get-Command node -ErrorAction SilentlyContinue
if ($null -eq $node) {
    Write-Warning "Node.js not found. JavaScript wrapper will not be minified."
    $nodeAvailable = $false
} else {
    $nodeAvailable = $true
}

# Check if Emscripten is available
$emcc = Get-Command emcc -ErrorAction SilentlyContinue
if ($null -eq $emcc) {
    Write-Error "Emscripten compiler (emcc) not found. Please install Emscripten SDK and activate it."
    Write-Host "Visit https://emscripten.org/docs/getting_started/downloads.html for installation instructions."
    
    # If Node.js is available, we can still process the JavaScript wrapper
    if ($nodeAvailable) {
        Write-Host "Proceeding with JavaScript wrapper processing only..."
        Set-Location $PSScriptRoot
        
        # Install dependencies if needed
        if (-not (Test-Path "node_modules")) {
            Write-Host "Installing Node.js dependencies..."
            npm install
        }
        
        # Copy and minify the JavaScript wrapper
        Write-Host "Processing JavaScript wrapper..."
        npm run build-wrapper
        
        Write-Host "JavaScript wrapper processed. WebAssembly module not built."
        exit 0
    }
    
    exit 1
}

# Create theme/wasm directory if it doesn't exist
$wasmDir = Join-Path ".." ".." "theme" "wasm"
if (-not (Test-Path $wasmDir)) {
    New-Item -ItemType Directory -Path $wasmDir -Force
}

# Navigate to build directory
$buildDir = Join-Path $PSScriptRoot "build"
if (-not (Test-Path $buildDir)) {
    New-Item -ItemType Directory -Path $buildDir -Force
}
Set-Location $buildDir

# Run CMake with Emscripten
Write-Host "Running CMake with Emscripten..."
emcmake cmake ..

# Build the project
Write-Host "Building WebAssembly module..."
cmake --build . --config Release

# Copy the built files to the theme directory if the build didn't handle it
$jsFile = Join-Path $buildDir "video_processor.js"
$wasmFile = Join-Path $buildDir "video_processor.wasm"
$targetDir = Join-Path ".." ".." ".." "theme" "wasm"

if ((Test-Path $jsFile) -and (Test-Path $wasmFile)) {
    Write-Host "Copying WebAssembly files to theme directory..."
    Copy-Item -Path $jsFile, $wasmFile -Destination $targetDir -Force
    Write-Host "WebAssembly module built successfully!"
} else {
    Write-Error "Failed to build WebAssembly module."
    exit 1
}

# Return to original directory to process JavaScript wrapper
Set-Location $PSScriptRoot

# Process the JavaScript wrapper
if ($nodeAvailable) {
    # Install dependencies if needed
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing Node.js dependencies..."
        npm install
    }
    
    # Minify and copy the JavaScript wrapper
    Write-Host "Processing JavaScript wrapper..."
    npm run build-wrapper
    
    Write-Host "JavaScript wrapper processed."
} else {
    # Just copy the JavaScript wrapper without minification
    Write-Host "Copying JavaScript wrapper without minification..."
    Copy-Item -Path "src/video_processor_wrapper.js" -Destination $wasmDir -Force
}

Write-Host "Build completed successfully!" 