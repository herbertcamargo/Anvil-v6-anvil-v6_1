<template>
  <div class="video-processor">
    <h2>WebAssembly Video Processor (Vue)</h2>
    
    <div class="controls">
      <input 
        type="file" 
        accept="video/*" 
        @change="handleFileChange" 
        class="file-input"
      />
      
      <button 
        @click="handlePlayPause" 
        :disabled="!videoFile || !wasmReady"
        class="play-button"
      >
        {{ isPlaying ? 'Pause' : 'Play' }}
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
        <video 
          ref="video" 
          :src="videoFile" 
          :style="{ display: videoFile ? 'block' : 'none' }"
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
export default {
  name: 'VideoProcessor',
  data() {
    return {
      videoFile: null,
      isPlaying: false,
      effectType: 0, // 0: grayscale, 1: sepia, 2: brightness, 3: blur
      effectParam: 1.0,
      wasmReady: false,
      processor: null,
      stopProcessing: null
    };
  },
  mounted() {
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
  },
  beforeUnmount() {
    // Clean up processing on unmount
    if (this.stopProcessing) {
      this.stopProcessing();
      this.stopProcessing = null;
    }
  },
  methods: {
    initProcessor() {
      this.processor = new window.VideoProcessorWrapper();
      this.processor.onReady(() => {
        this.wasmReady = true;
      });
    },
    handleFileChange(e) {
      const file = e.target.files[0];
      if (file) {
        const url = URL.createObjectURL(file);
        this.videoFile = url;
        
        if (this.$refs.video) {
          this.$refs.video.src = url;
        }
        
        // Stop current processing if any
        if (this.stopProcessing) {
          this.stopProcessing();
          this.stopProcessing = null;
        }
        
        this.isPlaying = false;
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