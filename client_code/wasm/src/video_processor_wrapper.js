/**
 * VideoProcessorWrapper - A JavaScript wrapper for the WebAssembly video processing module
 * This class provides an easy-to-use interface for applying video effects using WebAssembly
 */
class VideoProcessorWrapper {
  constructor() {
    this.module = null;
    this.processor = null;
    this.isReady = false;
    this.readyCallbacks = [];
    
    // Load the WebAssembly module
    this._loadModule();
  }
  
  /**
   * Loads the WebAssembly module
   * @private
   */
  _loadModule() {
    const scriptElement = document.createElement('script');
    scriptElement.src = '_/theme/wasm/video_processor.js';
    scriptElement.onload = () => {
      // Initialize the module
      VideoProcessorModule().then(module => {
        this.module = module;
        this.processor = new module.VideoProcessor();
        this.isReady = true;
        
        // Call any pending callbacks
        this.readyCallbacks.forEach(callback => callback());
        this.readyCallbacks = [];
      });
    };
    document.head.appendChild(scriptElement);
  }
  
  /**
   * Check if the module is ready, and if not, register a callback
   * @param {Function} callback - Function to call when the module is ready
   * @returns {boolean} - True if the module is ready, false if the callback was registered
   */
  onReady(callback) {
    if (this.isReady) {
      callback();
      return true;
    } else {
      this.readyCallbacks.push(callback);
      return false;
    }
  }
  
  /**
   * Process a canvas with the specified effect
   * @param {HTMLCanvasElement} canvas - The canvas to process
   * @param {number} effectType - Effect type (0: grayscale, 1: sepia, 2: brightness, 3: blur)
   * @param {number} param - Parameter for the effect (used by brightness and blur)
   */
  processCanvas(canvas, effectType, param = 1.0) {
    if (!this.isReady) {
      console.error('WebAssembly module not ready yet');
      return;
    }
    
    const ctx = canvas.getContext('2d');
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    
    // Create a pointer to the data in the WebAssembly memory
    const dataPtr = this.module._malloc(data.length);
    
    // Copy the image data to WebAssembly memory
    const heap = new Uint8Array(this.module.HEAPU8.buffer, dataPtr, data.length);
    heap.set(data);
    
    // Process the image with the selected effect
    if (effectType === 0) {
      this.processor.applyGrayscale(dataPtr, canvas.width, canvas.height);
    } else if (effectType === 1) {
      this.processor.applySepia(dataPtr, canvas.width, canvas.height);
    } else if (effectType === 2) {
      this.processor.adjustBrightness(dataPtr, canvas.width, canvas.height, param);
    } else if (effectType === 3) {
      this.processor.applyBlur(dataPtr, canvas.width, canvas.height, Math.round(param));
    } else {
      console.error('Unknown effect type:', effectType);
    }
    
    // Copy the processed data back to the image data
    const resultData = new Uint8Array(this.module.HEAPU8.buffer, dataPtr, data.length);
    data.set(resultData);
    
    // Free the allocated memory
    this.module._free(dataPtr);
    
    // Put the processed image data back to the canvas
    ctx.putImageData(imageData, 0, 0);
  }
  
  /**
   * Process a video frame
   * @param {HTMLVideoElement} video - The video element to process
   * @param {HTMLCanvasElement} canvas - The canvas to render the processed frame
   * @param {number} effectType - Effect type (0: grayscale, 1: sepia, 2: brightness, 3: blur)
   * @param {number} param - Parameter for the effect (used by brightness and blur)
   */
  processVideoFrame(video, canvas, effectType, param = 1.0) {
    if (!video.paused && !video.ended) {
      const ctx = canvas.getContext('2d');
      
      // Set canvas dimensions to match the video
      if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
      }
      
      // Draw the current video frame to the canvas
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      // Process the canvas with the selected effect
      this.processCanvas(canvas, effectType, param);
    }
  }
  
  /**
   * Start continuous processing of a video
   * @param {HTMLVideoElement} video - The video element to process
   * @param {HTMLCanvasElement} canvas - The canvas to render the processed frames
   * @param {number} effectType - Effect type (0: grayscale, 1: sepia, 2: brightness, 3: blur)
   * @param {number} param - Parameter for the effect (used by brightness and blur)
   * @returns {Function} - A function to stop the processing
   */
  startVideoProcessing(video, canvas, effectType, param = 1.0) {
    let isProcessing = true;
    
    const processFrame = () => {
      if (!isProcessing) return;
      
      this.processVideoFrame(video, canvas, effectType, param);
      requestAnimationFrame(processFrame);
    };
    
    processFrame();
    
    // Return a function to stop processing
    return () => {
      isProcessing = false;
    };
  }
}

// Export the wrapper for use in Anvil
window.VideoProcessorWrapper = VideoProcessorWrapper; 