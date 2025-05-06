#!/bin/bash

# Install dependencies
npm install

# Build components
npm run build

# Ensure target directory exists
TARGET_DIR="../.."
COMPONENTS_DIR="$TARGET_DIR/theme/components"

mkdir -p "$COMPONENTS_DIR"

# Copy built files to theme directory to be served by Anvil
cp -f ../js/components/*.js "$COMPONENTS_DIR/" 