import React, { useState, useEffect, useRef } from 'react';

const VideoProcessor = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [effectType, setEffectType] = useState(0); // 0: grayscale, 1: sepia, 2: brightness, 3: blur
  const [effectParam, setEffectParam] = useState(1.0);
  const [wasmReady, setWasmReady] = useState(false);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const processorRef = useRef(null);
  const stopProcessingRef = useRef(null);
  
  // Initialize WebAssembly processor
  useEffect(() => {
    // Check if the wrapper is already loaded
    if (window.VideoProcessorWrapper) {
      initProcessor();
    } else {
      // Load the wrapper script
      const script = document.createElement('script');
      script.src = '_/theme/wasm/video_processor_wrapper.js';
      script.onload = () => {
        initProcessor();
      };
      document.head.appendChild(script);
    }
    
    return () => {
      // Clean up processing on unmount
      if (stopProcessingRef.current) {
        stopProcessingRef.current();
        stopProcessingRef.current = null;
      }
    };
  }, []);
  
  const initProcessor = () => {
    processorRef.current = new window.VideoProcessorWrapper();
    processorRef.current.onReady(() => {
      setWasmReady(true);
    });
  };
  
  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setVideoFile(url);
      
      if (videoRef.current) {
        videoRef.current.src = url;
      }
      
      // Stop current processing if any
      if (stopProcessingRef.current) {
        stopProcessingRef.current();
        stopProcessingRef.current = null;
      }
      
      setIsPlaying(false);
    }
  };
  
  // Handle play/pause
  const handlePlayPause = () => {
    if (!videoRef.current || !videoFile) return;
    
    if (isPlaying) {
      videoRef.current.pause();
      
      // Stop processing
      if (stopProcessingRef.current) {
        stopProcessingRef.current();
        stopProcessingRef.current = null;
      }
    } else {
      videoRef.current.play();
      
      // Start processing
      if (wasmReady && processorRef.current) {
        stopProcessingRef.current = processorRef.current.startVideoProcessing(
          videoRef.current,
          canvasRef.current,
          effectType,
          effectParam
        );
      }
    }
    
    setIsPlaying(!isPlaying);
  };
  
  // Handle effect change
  const handleEffectChange = (e) => {
    const newEffectType = parseInt(e.target.value, 10);
    setEffectType(newEffectType);
    
    // Restart processing with new effect
    if (isPlaying && wasmReady && processorRef.current) {
      if (stopProcessingRef.current) {
        stopProcessingRef.current();
      }
      
      stopProcessingRef.current = processorRef.current.startVideoProcessing(
        videoRef.current,
        canvasRef.current,
        newEffectType,
        effectParam
      );
    }
  };
  
  // Handle effect parameter change
  const handleParamChange = (e) => {
    const newParam = parseFloat(e.target.value);
    setEffectParam(newParam);
    
    // Restart processing with new parameter
    if (isPlaying && wasmReady && processorRef.current) {
      if (stopProcessingRef.current) {
        stopProcessingRef.current();
      }
      
      stopProcessingRef.current = processorRef.current.startVideoProcessing(
        videoRef.current,
        canvasRef.current,
        effectType,
        newParam
      );
    }
  };
  
  return (
    <div className="video-processor">
      <h2>WebAssembly Video Processor</h2>
      
      <div className="controls">
        <input 
          type="file" 
          accept="video/*" 
          onChange={handleFileChange} 
          className="file-input"
        />
        
        <button 
          onClick={handlePlayPause} 
          disabled={!videoFile || !wasmReady}
          className="play-button"
        >
          {isPlaying ? 'Pause' : 'Play'}
        </button>
        
        <div className="effect-selector">
          <label>Effect: </label>
          <select value={effectType} onChange={handleEffectChange}>
            <option value={0}>Grayscale</option>
            <option value={1}>Sepia</option>
            <option value={2}>Brightness</option>
            <option value={3}>Blur</option>
          </select>
        </div>
        
        {(effectType === 2 || effectType === 3) && (
          <div className="param-slider">
            <label>
              {effectType === 2 ? 'Brightness: ' : 'Blur Radius: '}
              {effectParam.toFixed(1)}
            </label>
            <input 
              type="range" 
              min={effectType === 2 ? "0.1" : "1"} 
              max={effectType === 2 ? "3.0" : "10"} 
              step={effectType === 2 ? "0.1" : "1"} 
              value={effectParam}
              onChange={handleParamChange}
            />
          </div>
        )}
      </div>
      
      <div className="video-container">
        <div className="video-wrapper">
          <h3>Original</h3>
          <video 
            ref={videoRef} 
            src={videoFile} 
            controls={false} 
            style={{ display: videoFile ? 'block' : 'none' }}
          />
        </div>
        
        <div className="canvas-wrapper">
          <h3>Processed with WebAssembly</h3>
          <canvas 
            ref={canvasRef} 
            style={{ display: videoFile ? 'block' : 'none' }}
          />
        </div>
      </div>
      
      {!wasmReady && (
        <div className="loading">
          Loading WebAssembly module...
        </div>
      )}
      
      <style jsx>{`
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
          background-color: #4CAF50;
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
      `}</style>
    </div>
  );
};

export default VideoProcessor; 