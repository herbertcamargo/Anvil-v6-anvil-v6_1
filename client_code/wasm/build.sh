#!/bin/bash

# This script builds the WebAssembly module for video processing
# Note: You need to have Emscripten SDK installed and activated in your environment

# Message for users
echo "Building WebAssembly module for video processing..."

# Check if Node.js is available for JavaScript processing
if ! command -v node &> /dev/null; then
    echo "Warning: Node.js not found. JavaScript wrapper will not be minified."
    NODE_AVAILABLE=false
else
    NODE_AVAILABLE=true
fi

# Check if Emscripten is available
if ! command -v emcc &> /dev/null; then
    echo "Error: Emscripten compiler (emcc) not found. Please install Emscripten SDK and activate it."
    echo "Visit https://emscripten.org/docs/getting_started/downloads.html for installation instructions."
    
    # If Node.js is available, we can still process the JavaScript wrapper
    if [ "$NODE_AVAILABLE" = true ]; then
        echo "Proceeding with JavaScript wrapper processing only..."
        SCRIPT_DIR="$(pwd)"
        
        # Install dependencies if needed
        if [ ! -d "node_modules" ]; then
            echo "Installing Node.js dependencies..."
            npm install
        fi
        
        # Copy and minify the JavaScript wrapper
        echo "Processing JavaScript wrapper..."
        npm run build-wrapper
        
        echo "JavaScript wrapper processed. WebAssembly module not built."
        exit 0
    fi
    
    exit 1
fi

# Create theme/wasm directory if it doesn't exist
WASM_DIR="../../theme/wasm"
mkdir -p $WASM_DIR

# Navigate to build directory
SCRIPT_DIR="$(pwd)"
BUILD_DIR="${SCRIPT_DIR}/build"
mkdir -p $BUILD_DIR
cd $BUILD_DIR

# Run CMake with Emscripten
echo "Running CMake with Emscripten..."
emcmake cmake ..

# Build the project
echo "Building WebAssembly module..."
cmake --build . --config Release

# Copy the built files to the theme directory if the build didn't handle it
JS_FILE="${BUILD_DIR}/video_processor.js"
WASM_FILE="${BUILD_DIR}/video_processor.wasm"
TARGET_DIR="../../../theme/wasm"

if [ -f "$JS_FILE" ] && [ -f "$WASM_FILE" ]; then
    echo "Copying WebAssembly files to theme directory..."
    cp -f $JS_FILE $WASM_FILE $TARGET_DIR/
    echo "WebAssembly module built successfully!"
else
    echo "Error: Failed to build WebAssembly module."
    exit 1
fi

# Return to original directory to process JavaScript wrapper
cd "$SCRIPT_DIR"

# Process the JavaScript wrapper
if [ "$NODE_AVAILABLE" = true ]; then
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing Node.js dependencies..."
        npm install
    fi
    
    # Minify and copy the JavaScript wrapper
    echo "Processing JavaScript wrapper..."
    npm run build-wrapper
    
    echo "JavaScript wrapper processed."
else
    # Just copy the JavaScript wrapper without minification
    echo "Copying JavaScript wrapper without minification..."
    cp -f "src/video_processor_wrapper.js" $WASM_DIR/
fi

echo "Build completed successfully!" 