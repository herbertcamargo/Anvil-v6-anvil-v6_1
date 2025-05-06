# Install dependencies
npm install

# Build components
npm run build

# Ensure target directory exists
$targetDir = "../.."
$componentsDir = Join-Path $targetDir "theme/components"

if (-not (Test-Path $componentsDir)) {
    New-Item -ItemType Directory -Path $componentsDir -Force
}

# Copy built files to theme directory to be served by Anvil
Copy-Item -Path "../js/components/*.js" -Destination $componentsDir -Force 