<template>
  <div class="video-processor vue">
    <h2>WebAssembly Video Processor (Vue)</h2>
    
    <div v-if="isOffline" class="offline-banner">
      <p>You are currently offline. {{ isVideoSavedOffline ? 
        'This video is available for offline use.' : 
        'Some features may be limited.' }}
      </p>
    </div>
    
    <div class="controls">
      <input 
        type="file" 
        accept="video/*" 
        @change="handleFileChange" 
        class="file-input"
        ref="fileInput"
        :disabled="isOffline && !isVideoSavedOffline"
      />
      
      <button 
        @click="handlePlayPause" 
        :disabled="!videoFile || !wasmReady"
        class="play-button"
      >
        {{ isPlaying ? 'Pause' : 'Play' }}
      </button>
      
      <button 
        v-if="videoFile && !isVideoSavedOffline && !isOffline"
        @click="saveVideoForOffline"
        class="save-offline-button"
      >
        Save for Offline
      </button>
      
      <div class="effect-selector">
        <label>Effect: </label>
        <select v-model="effectType" @change="handleEffectChange">
          <option :value="0">Grayscale</option>
          <option :value="1">Sepia</option>
          <option :value="2">Brightness</option>
          <option :value="3">Blur</option>
        </select>
      </div>
      
      <div v-if="effectType === 2 || effectType === 3" class="param-slider">
        <label>
          {{ effectType === 2 ? 'Brightness: ' : 'Blur Radius: ' }}
          {{ effectParam.toFixed(1) }}
        </label>
        <input 
          type="range" 
          :min="effectType === 2 ? 0.1 : 1" 
          :max="effectType === 2 ? 3.0 : 10" 
          :step="effectType === 2 ? 0.1 : 1" 
          v-model="effectParam"
          @input="handleParamChange"
        />
      </div>
    </div>
    
    <div class="video-container">
      <div class="video-wrapper">
        <h3>Original</h3>
        <img 
          v-if="thumbnailUrl && !isPlaying"
          :src="thumbnailUrl" 
          alt="Video thumbnail" 
          class="video-thumbnail"
        />
        <video 
          ref="video" 
          :src="videoFile" 
          :style="{ display: videoFile && (!thumbnailUrl || isPlaying) ? 'block' : 'none' }"
          @loadedmetadata="onVideoLoad"
        />
      </div>
      
      <div class="canvas-wrapper">
        <h3>Processed with WebAssembly</h3>
        <canvas 
          ref="canvas" 
          :style="{ display: videoFile ? 'block' : 'none' }"
        />
      </div>
    </div>
    
    <div v-if="!wasmReady" class="loading">
      Loading WebAssembly module...
    </div>
  </div>
</template>

<script>
import { 
  registerServiceWorker, 
  storeVideoForOffline, 
  getOfflineVideo, 
  createAndCacheVideoThumbnail, 
  isVideoAvailableOffline 
} from '../service-worker-registration';

export default {
  name: 'VideoProcessor',
  data() {
    return {
      videoFile: null,
      videoFileName: null,
      videoId: null,
      isPlaying: false,
      effectType: 0, // 0: grayscale, 1: sepia, 2: brightness, 3: blur
      effectParam: 1.0,
      wasmReady: false,
      isOffline: !navigator.onLine,
      isVideoSavedOffline: false,
      thumbnailUrl: null,
      processor: null,
      stopProcessing: null
    };
  },
  mounted() {
    // Register service worker
    registerServiceWorker();
    
    // Initialize WebAssembly processor
    if (window.VideoProcessorWrapper) {
      this.initProcessor();
    } else {
      // Load the wrapper script
      const script = document.createElement('script');
      script.src = '_/theme/wasm/video_processor_wrapper.js';
      script.onload = () => {
        this.initProcessor();
      };
      document.head.appendChild(script);
    }
    
    // Monitor online/offline status
    window.addEventListener('online', this.handleOnlineStatusChange);
    window.addEventListener('offline', this.handleOnlineStatusChange);
  },
  beforeUnmount() {
    // Clean up processing on unmount
    if (this.stopProcessing) {
      this.stopProcessing();
      this.stopProcessing = null;
    }
    
    window.removeEventListener('online', this.handleOnlineStatusChange);
    window.removeEventListener('offline', this.handleOnlineStatusChange);
  },
  watch: {
    isOffline(newValue) {
      if (newValue && this.videoId) {
        this.checkOfflineAvailability(this.videoId);
      }
    }
  },
  methods: {
    initProcessor() {
      this.processor = new window.VideoProcessorWrapper();
      this.processor.onReady(() => {
        this.wasmReady = true;
      });
    },
    handleOnlineStatusChange() {
      this.isOffline = !navigator.onLine;
    },
    async checkOfflineAvailability(id) {
      const available = await isVideoAvailableOffline(id);
      this.isVideoSavedOffline = available;
      
      // If we're offline and the video is available, load it
      if (this.isOffline && available) {
        this.loadOfflineVideo(id);
      }
    },
    async loadOfflineVideo(id) {
      try {
        const { videoData, metadata } = await getOfflineVideo(id);
        
        if (videoData && this.$refs.video) {
          // Create a blob from the stored data
          const blob = new Blob([videoData], { type: metadata.type });
          const url = URL.createObjectURL(blob);
          
          this.videoFile = url;
          this.videoFileName = metadata.name;
          this.$refs.video.src = url;
          
          // Set thumbnail if available
          if (metadata.thumbnailUrl) {
            this.thumbnailUrl = metadata.thumbnailUrl;
          }
        }
      } catch (error) {
        console.error('Failed to load offline video:', error);
      }
    },
    async saveVideoForOffline() {
      if (!this.videoFile || !this.$refs.video || !this.videoId) return;
      
      try {
        // Get the video data
        const response = await fetch(this.videoFile);
        const videoBlob = await response.blob();
        const videoArrayBuffer = await videoBlob.arrayBuffer();
        
        // Create and cache a thumbnail
        const thumbUrl = await createAndCacheVideoThumbnail(this.videoId, this.$refs.video);
        
        // Save to IndexedDB
        await storeVideoForOffline(this.videoId, videoArrayBuffer, {
          name: this.videoFileName,
          type: videoBlob.type,
          size: videoBlob.size,
          thumbnailUrl: thumbUrl,
          timestamp: new Date().getTime()
        });
        
        this.isVideoSavedOffline = true;
        this.thumbnailUrl = thumbUrl;
        
        // Show success notification
        if ('Notification' in window && Notification.permission === 'granted') {
          new Notification('Video Saved Offline', {
            body: `${this.videoFileName} is now available for offline use.`,
            icon: thumbUrl
          });
        }
      } catch (error) {
        console.error('Failed to save video for offline use:', error);
      }
    },
    handleFileChange(e) {
      const file = e.target.files[0];
      if (file) {
        const url = URL.createObjectURL(file);
        this.videoFile = url;
        this.videoFileName = file.name;
        
        // Generate a unique ID for this video
        this.videoId = `video_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        if (this.$refs.video) {
          this.$refs.video.src = url;
        }
        
        // Stop current processing if any
        if (this.stopProcessing) {
          this.stopProcessing();
          this.stopProcessing = null;
        }
        
        this.isPlaying = false;
        this.isVideoSavedOffline = false;
        this.thumbnailUrl = null;
      }
    },
    onVideoLoad() {
      if (this.videoId && !this.thumbnailUrl) {
        createAndCacheVideoThumbnail(this.videoId, this.$refs.video)
          .then(url => this.thumbnailUrl = url)
          .catch(err => console.error('Error creating thumbnail:', err));
      }
    },
    handlePlayPause() {
      if (!this.$refs.video || !this.videoFile) return;
      
      if (this.isPlaying) {
        this.$refs.video.pause();
        
        // Stop processing
        if (this.stopProcessing) {
          this.stopProcessing();
          this.stopProcessing = null;
        }
      } else {
        this.$refs.video.play();
        
        // Start processing
        if (this.wasmReady && this.processor) {
          this.stopProcessing = this.processor.startVideoProcessing(
            this.$refs.video,
            this.$refs.canvas,
            this.effectType,
            this.effectParam
          );
          
          // Create thumbnail after a short delay if none exists
          if (!this.thumbnailUrl && this.videoId) {
            setTimeout(async () => {
              try {
                const thumbUrl = await createAndCacheVideoThumbnail(this.videoId, this.$refs.video);
                this.thumbnailUrl = thumbUrl;
              } catch (error) {
                console.error('Failed to create thumbnail:', error);
              }
            }, 500);
          }
        }
      }
      
      this.isPlaying = !this.isPlaying;
    },
    handleEffectChange() {
      // Restart processing with new effect
      this.restartProcessing();
    },
    handleParamChange() {
      // Convert string to number 
      this.effectParam = parseFloat(this.effectParam);
      // Restart processing with new parameter
      this.restartProcessing();
    },
    restartProcessing() {
      if (this.isPlaying && this.wasmReady && this.processor) {
        if (this.stopProcessing) {
          this.stopProcessing();
        }
        
        this.stopProcessing = this.processor.startVideoProcessing(
          this.$refs.video,
          this.$refs.canvas,
          this.effectType,
          this.effectParam
        );
      }
    }
  }
};
</script>

<style scoped>
.video-processor {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.controls {
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: center;
}

.file-input {
  flex: 1;
  min-width: 200px;
}

.play-button {
  padding: 8px 15px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.play-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.save-offline-button {
  padding: 8px 15px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.offline-banner {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
}

.effect-selector, .param-slider {
  display: flex;
  align-items: center;
  gap: 8px;
}

.video-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.video-wrapper, .canvas-wrapper {
  flex: 1;
  min-width: 300px;
}

video, canvas {
  width: 100%;
  background-color: #000;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.video-thumbnail {
  width: 100%;
  background-color: #000;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.loading {
  margin-top: 20px;
  padding: 10px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
}
</style>