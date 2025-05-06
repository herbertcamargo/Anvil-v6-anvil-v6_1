// React hooks for using GraphQL in Anvil components
import { useState, useEffect } from 'react';
import { executeQuery, Queries } from './client';

/**
 * Hook to search YouTube videos using GraphQL
 * @param {string} initialQuery - Initial search query
 * @param {number} maxResults - Maximum number of results to return
 * @returns {Object} - { videos, loading, error, search }
 */
export function useYouTubeSearch(initialQuery = '', maxResults = 12) {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Function to perform search
  const search = async (query) => {
    if (!query) {
      setVideos([]);
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await executeQuery(Queries.SEARCH_VIDEOS, {
        query,
        maxResults
      });
      
      setVideos(data.searchVideos || []);
    } catch (err) {
      setError(err.message || 'Error searching videos');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // Run initial search if provided
  useEffect(() => {
    if (initialQuery) {
      search(initialQuery);
    }
  }, [initialQuery]);
  
  return { videos, loading, error, search };
}

/**
 * Hook to get a specific YouTube video with transcript
 * @param {string} videoId - YouTube video ID
 * @returns {Object} - { video, transcript, loading, error }
 */
export function useYouTubeVideo(videoId) {
  const [video, setVideo] = useState(null);
  const [transcript, setTranscript] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchVideo = async () => {
      if (!videoId) return;
      
      setLoading(true);
      setError(null);
      
      try {
        const data = await executeQuery(Queries.GET_VIDEO_WITH_TRANSCRIPT, {
          id: videoId
        });
        
        if (data.videoWithTranscript) {
          setVideo({
            id: data.videoWithTranscript.id,
            title: data.videoWithTranscript.snippet?.title || '',
            description: data.videoWithTranscript.snippet?.description || ''
          });
          
          setTranscript(data.videoWithTranscript.transcript || []);
        } else {
          setError('Video not found');
        }
      } catch (err) {
        setError(err.message || 'Error fetching video');
        console.error('Video fetch error:', err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchVideo();
  }, [videoId]);
  
  return { video, transcript, loading, error };
}

/**
 * Hook to only fetch the transcript for a video
 * @param {string} videoId - YouTube video ID
 * @returns {Object} - { transcript, loading, error }
 */
export function useYouTubeTranscript(videoId) {
  const [transcript, setTranscript] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchTranscript = async () => {
      if (!videoId) return;
      
      setLoading(true);
      setError(null);
      
      try {
        const data = await executeQuery(Queries.GET_TRANSCRIPT, {
          id: videoId
        });
        
        if (data.videoWithTranscript) {
          setTranscript(data.videoWithTranscript.transcript || []);
        } else {
          setError('Transcript not found');
        }
      } catch (err) {
        setError(err.message || 'Error fetching transcript');
        console.error('Transcript fetch error:', err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchTranscript();
  }, [videoId]);
  
  return { transcript, loading, error };
} 