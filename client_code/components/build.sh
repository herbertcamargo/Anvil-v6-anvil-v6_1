#!/bin/bash

# Build script for Anvil modern components (React, Vue, Service Worker)

echo "Building modern components for Anvil application..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js not found. Please install Node.js to build components."
    echo "Visit https://nodejs.org/ for installation instructions."
    exit 1
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Build the components
echo "Building React and Vue components..."
npm run build

# Build service worker
echo "Building Service Worker..."
npm run build-sw

echo "Build completed successfully!"

# Ensure target directory exists
TARGET_DIR="../.."
COMPONENTS_DIR="$TARGET_DIR/theme/components"

mkdir -p "$COMPONENTS_DIR"

# Copy built files to theme directory to be served by Anvil
cp -f ../js/components/*.js "$COMPONENTS_DIR/" 