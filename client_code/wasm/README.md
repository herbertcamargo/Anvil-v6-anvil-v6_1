# WebAssembly for Anvil

This directory contains WebAssembly modules to perform high-performance operations in your Anvil application, particularly for video processing tasks.

## Prerequisites

To build the WebAssembly modules, you'll need:

1. [Emscripten SDK](https://emscripten.org/docs/getting_started/downloads.html) - for compiling C/C++ to WebAssembly
2. [CMake](https://cmake.org/download/) - for building the C/C++ code
3. [Node.js and npm](https://nodejs.org/) - for JavaScript tooling

## Project Structure

- `src/` - Source code for WebAssembly modules
  - `video_processor.cpp` - C++ implementation of video processing functions
  - `video_processor_wrapper.js` - JavaScript wrapper for WebAssembly video processor
- `build/` - Build output directory
- `build.ps1` - PowerShell build script for Windows
- `build.sh` - Bash build script for Mac/Linux
- `CMakeLists.txt` - CMake configuration

## Building the WebAssembly Module

### On Windows

```powershell
# Navigate to this directory
cd client_code/wasm

# Activate Emscripten environment first
# Example: call emsdk_env.bat from your Emscripten installation

# Run the build script
./build.ps1
```

### On Mac/Linux

```bash
# Navigate to this directory
cd client_code/wasm

# Activate Emscripten environment first
# Example: source ./emsdk_env.sh from your Emscripten installation

# Make the build script executable
chmod +x build.sh

# Run the build script
./build.sh
```

## Using WebAssembly in Anvil

The build process will create two main files in the `theme/wasm/` directory:

1. `video_processor.js` and `video_processor.wasm` - The compiled WebAssembly module
2. `video_processor_wrapper.js` - A JavaScript wrapper to make it easier to use the WebAssembly module

### Via React/Vue Components

The easiest way to use the WebAssembly video processor is through the provided React and Vue components:

1. Make sure the WebAssembly module is built and placed in the theme directory
2. Use the VideoProcessor component in your Anvil app

Example:

```python
# In your Anvil form Python code
import anvil.js

# For React
anvil.js.call_js('window.renderReactComponent', 'VideoProcessor', 'container-id')

# For Vue
anvil.js.call_js('window.renderVueComponent', 'VideoProcessor', 'container-id')
```

### Directly in JavaScript

You can also use the WebAssembly module directly in JavaScript:

```python
# In your Anvil form Python code
anvil.js.call_js('eval', """
  // Load the wrapper script
  const script = document.createElement('script');
  script.src = '_/theme/wasm/video_processor_wrapper.js';
  script.onload = function() {
    // Initialize the processor
    const processor = new window.VideoProcessorWrapper();
    
    // Use the processor when it's ready
    processor.onReady(() => {
      const canvas = document.getElementById('my-canvas');
      // Apply an effect (0: grayscale, 1: sepia, 2: brightness, 3: blur)
      processor.processCanvas(canvas, 0);
    });
  };
  document.head.appendChild(script);
""")
```

## Supported Video Processing Operations

The WebAssembly module provides these main functions:

1. **Grayscale** - Convert images/video to grayscale
2. **Sepia** - Apply a sepia tone effect
3. **Brightness** - Adjust the brightness level
4. **Blur** - Apply a box blur effect with controllable radius

## Performance Benefits

WebAssembly provides near-native performance for computationally intensive tasks like video processing. Some advantages include:

1. **Speed** - Much faster than equivalent JavaScript for pixel manipulation
2. **Efficiency** - Lower CPU usage for the same operations
3. **Consistency** - More predictable performance across browsers

This makes it ideal for real-time video processing where JavaScript alone might struggle to maintain smooth framerates. 