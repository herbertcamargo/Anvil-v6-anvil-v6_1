# Build script for Anvil modern components (React, Vue, Service Worker)

Write-Host "Building modern components for Anvil application..."

# Check if Node.js is installed
$node = Get-Command node -ErrorAction SilentlyContinue
if ($null -eq $node) {
    Write-Error "Node.js not found. Please install Node.js to build components."
    Write-Host "Visit https://nodejs.org/ for installation instructions."
    exit 1
}

# Install dependencies if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing Node.js dependencies..."
    npm install
}

# Build the components
Write-Host "Building React and Vue components..."
npm run build

# Build service worker
Write-Host "Building Service Worker..."
npm run build-sw

Write-Host "Build completed successfully!"

# Ensure target directory exists
$targetDir = "../.."
$componentsDir = Join-Path $targetDir "theme/components"

if (-not (Test-Path $componentsDir)) {
    New-Item -ItemType Directory -Path $componentsDir -Force
}

# Copy built files to theme directory to be served by Anvil
Copy-Item -Path "../js/components/*.js" -Destination $componentsDir -Force 