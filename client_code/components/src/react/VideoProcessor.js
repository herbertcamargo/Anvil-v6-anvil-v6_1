import React, { useState, useEffect, useRef } from 'react';
import { 
  registerServiceWorker, 
  storeVideoForOffline, 
  getOfflineVideo, 
  createAndCacheVideoThumbnail, 
  isVideoAvailableOffline
} from '../service-worker-registration';

const VideoProcessor = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [videoFileName, setVideoFileName] = useState(null);
  const [videoId, setVideoId] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [effectType, setEffectType] = useState(0); // 0: grayscale, 1: sepia, 2: brightness, 3: blur
  const [effectParam, setEffectParam] = useState(1.0);
  const [wasmReady, setWasmReady] = useState(false);
  const [isOffline, setIsOffline] = useState(!navigator.onLine);
  const [isVideoSavedOffline, setIsVideoSavedOffline] = useState(false);
  const [thumbnailUrl, setThumbnailUrl] = useState(null);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const processorRef = useRef(null);
  const stopProcessingRef = useRef(null);
  const fileInputRef = useRef(null);
  
  // Initialize WebAssembly processor and service worker
  useEffect(() => {
    // Register service worker
    registerServiceWorker();
    
    // Initialize WebAssembly
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
    
    // Monitor online/offline status
    const handleOnlineStatusChange = () => {
      setIsOffline(!navigator.onLine);
    };
    
    window.addEventListener('online', handleOnlineStatusChange);
    window.addEventListener('offline', handleOnlineStatusChange);
    
    return () => {
      // Clean up processing on unmount
      if (stopProcessingRef.current) {
        stopProcessingRef.current();
        stopProcessingRef.current = null;
      }
      
      window.removeEventListener('online', handleOnlineStatusChange);
      window.removeEventListener('offline', handleOnlineStatusChange);
    };
  }, []);
  
  // Check if current video is available offline when offline status changes
  useEffect(() => {
    if (videoId && isOffline) {
      checkOfflineAvailability(videoId);
    }
  }, [videoId, isOffline]);
  
  const initProcessor = () => {
    processorRef.current = new window.VideoProcessorWrapper();
    processorRef.current.onReady(() => {
      setWasmReady(true);
    });
  };
  
  // Check if a video is available offline
  const checkOfflineAvailability = async (id) => {
    const available = await isVideoAvailableOffline(id);
    setIsVideoSavedOffline(available);
    
    // If we're offline and the video is available, load it
    if (isOffline && available) {
      loadOfflineVideo(id);
    }
  };
  
  // Load video from offline storage
  const loadOfflineVideo = async (id) => {
    try {
      const { videoData, metadata } = await getOfflineVideo(id);
      
      if (videoData && videoRef.current) {
        // Create a blob from the stored data
        const blob = new Blob([videoData], { type: metadata.type });
        const url = URL.createObjectURL(blob);
        
        setVideoFile(url);
        setVideoFileName(metadata.name);
        videoRef.current.src = url;
        
        // Set thumbnail if available
        if (metadata.thumbnailUrl) {
          setThumbnailUrl(metadata.thumbnailUrl);
        }
      }
    } catch (error) {
      console.error('Failed to load offline video:', error);
    }
  };
  
  // Save video for offline use
  const saveVideoForOffline = async () => {
    if (!videoFile || !videoRef.current || !videoId) return;
    
    try {
      // Get the video data
      const response = await fetch(videoFile);
      const videoBlob = await response.blob();
      const videoArrayBuffer = await videoBlob.arrayBuffer();
      
      // Create and cache a thumbnail
      const thumbUrl = await createAndCacheVideoThumbnail(videoId, videoRef.current);
      
      // Save to IndexedDB
      await storeVideoForOffline(videoId, videoArrayBuffer, {
        name: videoFileName,
        type: videoBlob.type,
        size: videoBlob.size,
        thumbnailUrl: thumbUrl,
        timestamp: new Date().getTime()
      });
      
      setIsVideoSavedOffline(true);
      setThumbnailUrl(thumbUrl);
      
      // Show success notification
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('Video Saved Offline', {
          body: `${videoFileName} is now available for offline use.`,
          icon: thumbUrl
        });
      }
    } catch (error) {
      console.error('Failed to save video for offline use:', error);
    }
  };
  
  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setVideoFile(url);
      setVideoFileName(file.name);
      
      // Generate a unique ID for this video
      const newVideoId = `video_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      setVideoId(newVideoId);
      
      if (videoRef.current) {
        videoRef.current.src = url;
      }
      
      // Stop current processing if any
      if (stopProcessingRef.current) {
        stopProcessingRef.current();
        stopProcessingRef.current = null;
      }
      
      setIsPlaying(false);
      setIsVideoSavedOffline(false);
      setThumbnailUrl(null);
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
        
        // Create thumbnail after a short delay if none exists
        if (!thumbnailUrl && videoId) {
          setTimeout(async () => {
            try {
              const thumbUrl = await createAndCacheVideoThumbnail(videoId, videoRef.current);
              setThumbnailUrl(thumbUrl);
            } catch (error) {
              console.error('Failed to create thumbnail:', error);
            }
          }, 500);
        }
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
      
      {isOffline && (
        <div className="offline-banner">
          <p>You are currently offline. {isVideoSavedOffline ? 
            'This video is available for offline use.' : 
            'Some features may be limited.'}
          </p>
        </div>
      )}
      
      <div className="controls">
        <input 
          type="file" 
          accept="video/*" 
          onChange={handleFileChange} 
          className="file-input"
          ref={fileInputRef}
          disabled={isOffline && !isVideoSavedOffline}
        />
        
        <button 
          onClick={handlePlayPause} 
          disabled={!videoFile || !wasmReady}
          className="play-button"
        >
          {isPlaying ? 'Pause' : 'Play'}
        </button>
        
        {videoFile && !isVideoSavedOffline && !isOffline && (
          <button 
            onClick={saveVideoForOffline}
            className="save-offline-button"
          >
            Save for Offline
          </button>
        )}
        
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
          {thumbnailUrl && !isPlaying && (
            <img 
              src={thumbnailUrl} 
              alt="Video thumbnail" 
              className="video-thumbnail"
              style={{ display: videoFile && !isPlaying ? 'block' : 'none' }}
            />
          )}
          <video 
            ref={videoRef} 
            src={videoFile} 
            controls={false} 
            style={{ display: videoFile && (!thumbnailUrl || isPlaying) ? 'block' : 'none' }}
            onLoadedMetadata={() => {
              if (videoId && !thumbnailUrl) {
                createAndCacheVideoThumbnail(videoId, videoRef.current)
                  .then(url => setThumbnailUrl(url))
                  .catch(err => console.error('Error creating thumbnail:', err));
              }
            }}
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
        
        .offline-banner {
          background-color: #f8f9fa;
          padding: 10px;
          border-radius: 4px;
          margin-bottom: 20px;
        }
        
        .save-offline-button {
          padding: 8px 15px;
          background-color: #4CAF50;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }
        
        .save-offline-button:disabled {
          background-color: #cccccc;
          cursor: not-allowed;
        }
        
        .video-thumbnail {
          width: 100%;
          height: auto;
          object-fit: cover;
          border-radius: 4px;
          margin-bottom: 10px;
        }
      `}</style>
    </div>
  );
};

export default VideoProcessor; 