# This script builds the SASS files and copies them to the theme directory

# Message for users
Write-Host "Building SASS files for Anvil application..."

# Check if Node.js is available
$node = Get-Command node -ErrorAction SilentlyContinue
if ($null -eq $node) {
    Write-Error "Node.js not found. Please install Node.js to build SASS files."
    Write-Host "Visit https://nodejs.org/ for installation instructions."
    exit 1
}

# Create theme/css directory if it doesn't exist
$cssDir = Join-Path ".." ".." "theme" "css"
if (-not (Test-Path $cssDir)) {
    New-Item -ItemType Directory -Path $cssDir -Force
}

# Install dependencies if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing Node.js dependencies..."
    npm install
}

# Build and copy the CSS files
Write-Host "Building SASS files and copying to theme directory..."
npm run build-and-copy

Write-Host "SASS build completed successfully!" 