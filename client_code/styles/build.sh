#!/bin/bash

# This script builds the SASS files and copies them to the theme directory

# Message for users
echo "Building SASS files for Anvil application..."

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "Error: Node.js not found. Please install Node.js to build SASS files."
    echo "Visit https://nodejs.org/ for installation instructions."
    exit 1
fi

# Create theme/css directory if it doesn't exist
CSS_DIR="../../theme/css"
mkdir -p $CSS_DIR

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Build and copy the CSS files
echo "Building SASS files and copying to theme directory..."
npm run build-and-copy

echo "SASS build completed successfully!" 