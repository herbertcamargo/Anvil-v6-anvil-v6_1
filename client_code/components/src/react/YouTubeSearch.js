import React, { useState, useEffect } from 'react';
import { reactHooks } from '../../../graphql';

const { useYouTubeSearch, useYouTubeVideo } = reactHooks;

// YouTube Search Component using GraphQL
const YouTubeSearch = ({ onVideoSelect }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentQuery, setCurrentQuery] = useState('');
  const [selectedVideoId, setSelectedVideoId] = useState(null);
  
  // Use our GraphQL hook to search videos
  const { videos, loading, error, search } = useYouTubeSearch();
  
  // Use our GraphQL hook to fetch selected video details
  const { 
    video: selectedVideo, 
    transcript, 
    loading: videoLoading 
  } = useYouTubeVideo(selectedVideoId);
  
  // Handle search submission
  const handleSubmit = (e) => {
    e.preventDefault();
    setCurrentQuery(searchTerm);
    search(searchTerm);
  };
  
  // Handle video selection
  const handleVideoSelect = (video) => {
    setSelectedVideoId(video.id);
    if (onVideoSelect) {
      onVideoSelect(video);
    }
  };
  
  // Notify parent when transcript is loaded
  useEffect(() => {
    if (selectedVideo && transcript && onVideoSelect) {
      onVideoSelect({
        ...selectedVideo,
        transcript
      });
    }
  }, [selectedVideo, transcript]);
  
  return (
    <div className="youtube-search">
      <h2>Search YouTube Videos</h2>
      
      {/* Search form */}
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search for videos..."
          className="search-input"
        />
        <button type="submit" className="search-button">Search</button>
      </form>
      
      {/* Loading state */}
      {loading && <div className="loading">Searching videos...</div>}
      
      {/* Error state */}
      {error && <div className="error">Error: {error}</div>}
      
      {/* Video results */}
      {videos.length > 0 && (
        <div className="search-results">
          <h3>Search Results for "{currentQuery}"</h3>
          <div className="video-grid">
            {videos.map(video => (
              <div 
                key={video.id} 
                className={`video-card ${selectedVideoId === video.id ? 'selected' : ''}`}
                onClick={() => handleVideoSelect(video)}
              >
                <div className="thumbnail-container">
                  <img 
                    src={video.thumbnail_url} 
                    alt={video.title} 
                    className="thumbnail" 
                  />
                </div>
                <div className="video-info">
                  <h4 className="video-title">{video.title}</h4>
                  <p className="channel-name">{video.channel.title}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* No results state */}
      {!loading && videos.length === 0 && currentQuery && (
        <div className="no-results">No videos found for "{currentQuery}"</div>
      )}
      
      <style jsx>{`
        .youtube-search {
          font-family: Arial, sans-serif;
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
        }
        
        .search-form {
          display: flex;
          margin-bottom: 20px;
        }
        
        .search-input {
          flex: 1;
          padding: 10px;
          font-size: 16px;
          border: 1px solid #ddd;
          border-radius: 4px 0 0 4px;
        }
        
        .search-button {
          padding: 10px 20px;
          background-color: #4CAF50;
          color: white;
          border: none;
          border-radius: 0 4px 4px 0;
          cursor: pointer;
        }
        
        .video-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
          gap: 20px;
        }
        
        .video-card {
          background-color: white;
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          cursor: pointer;
          transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .video-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .video-card.selected {
          border: 2px solid #4CAF50;
        }
        
        .thumbnail-container {
          position: relative;
          width: 100%;
          padding-top: 56.25%; /* 16:9 aspect ratio */
        }
        
        .thumbnail {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
        
        .video-info {
          padding: 15px;
        }
        
        .video-title {
          margin: 0 0 10px 0;
          font-size: 16px;
          line-height: 1.3;
          max-height: 2.6em;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
        }
        
        .channel-name {
          margin: 0;
          font-size: 14px;
          color: #606060;
        }
        
        .loading, .error, .no-results {
          padding: 20px;
          text-align: center;
          background-color: #f8f9fa;
          border-radius: 4px;
          margin-bottom: 20px;
        }
        
        .error {
          background-color: #ffebee;
          color: #c62828;
        }
      `}</style>
    </div>
  );
};

export default YouTubeSearch; 