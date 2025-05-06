// Vue composables for using GraphQL in Anvil Vue components
import { ref, reactive, watch } from 'vue';
import { executeQuery, Queries } from './client';

/**
 * Composable to search YouTube videos using GraphQL
 * @param {string} initialQuery - Initial search query
 * @param {number} maxResults - Maximum number of results to return
 * @returns {Object} - { videos, loading, error, search }
 */
export function useYouTubeSearch(initialQuery = '', maxResults = 12) {
  const videos = ref([]);
  const loading = ref(false);
  const error = ref(null);
  
  // Function to perform search
  const search = async (query) => {
    if (!query) {
      videos.value = [];
      return;
    }
    
    loading.value = true;
    error.value = null;
    
    try {
      const data = await executeQuery(Queries.SEARCH_VIDEOS, {
        query,
        maxResults
      });
      
      videos.value = data.searchVideos || [];
    } catch (err) {
      error.value = err.message || 'Error searching videos';
      console.error('Search error:', err);
    } finally {
      loading.value = false;
    }
  };
  
  // Perform initial search if provided
  if (initialQuery) {
    search(initialQuery);
  }
  
  return { videos, loading, error, search };
}

/**
 * Composable to get a specific YouTube video with transcript
 * @param {Ref<string>} videoId - Reactive YouTube video ID
 * @returns {Object} - { video, transcript, loading, error }
 */
export function useYouTubeVideo(videoId) {
  const video = ref(null);
  const transcript = ref([]);
  const loading = ref(false);
  const error = ref(null);
  
  // Watch for changes to videoId
  watch(videoId, async (newVideoId) => {
    if (!newVideoId) return;
    
    loading.value = true;
    error.value = null;
    
    try {
      const data = await executeQuery(Queries.GET_VIDEO_WITH_TRANSCRIPT, {
        id: newVideoId
      });
      
      if (data.videoWithTranscript) {
        video.value = {
          id: data.videoWithTranscript.id,
          title: data.videoWithTranscript.snippet?.title || '',
          description: data.videoWithTranscript.snippet?.description || ''
        };
        
        transcript.value = data.videoWithTranscript.transcript || [];
      } else {
        error.value = 'Video not found';
      }
    } catch (err) {
      error.value = err.message || 'Error fetching video';
      console.error('Video fetch error:', err);
    } finally {
      loading.value = false;
    }
  }, { immediate: true });
  
  return { video, transcript, loading, error };
}

/**
 * Composable to only fetch the transcript for a video
 * @param {Ref<string>} videoId - Reactive YouTube video ID
 * @returns {Object} - { transcript, loading, error }
 */
export function useYouTubeTranscript(videoId) {
  const transcript = ref([]);
  const loading = ref(false);
  const error = ref(null);
  
  // Watch for changes to videoId
  watch(videoId, async (newVideoId) => {
    if (!newVideoId) return;
    
    loading.value = true;
    error.value = null;
    
    try {
      const data = await executeQuery(Queries.GET_TRANSCRIPT, {
        id: newVideoId
      });
      
      if (data.videoWithTranscript) {
        transcript.value = data.videoWithTranscript.transcript || [];
      } else {
        error.value = 'Transcript not found';
      }
    } catch (err) {
      error.value = err.message || 'Error fetching transcript';
      console.error('Transcript fetch error:', err);
    } finally {
      loading.value = false;
    }
  }, { immediate: true });
  
  return { transcript, loading, error };
} 