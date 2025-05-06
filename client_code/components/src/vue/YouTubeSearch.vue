<template>
  <div class="youtube-search">
    <h2>Search YouTube Videos (Vue)</h2>
    
    <!-- Search form -->
    <form @submit.prevent="handleSubmit" class="search-form">
      <input
        type="text"
        v-model="searchTerm"
        placeholder="Search for videos..."
        class="search-input"
      />
      <button type="submit" class="search-button">Search</button>
    </form>
    
    <!-- Loading state -->
    <div v-if="loading" class="loading">Searching videos...</div>
    
    <!-- Error state -->
    <div v-if="error" class="error">Error: {{ error }}</div>
    
    <!-- Video results -->
    <div v-if="videos.length > 0" class="search-results">
      <h3>Search Results for "{{ currentQuery }}"</h3>
      <div class="video-grid">
        <div 
          v-for="video in videos" 
          :key="video.id" 
          class="video-card"
          :class="{ 'selected': selectedVideoId === video.id }"
          @click="handleVideoSelect(video)"
        >
          <div class="thumbnail-container">
            <img 
              :src="video.thumbnail_url" 
              :alt="video.title" 
              class="thumbnail" 
            />
          </div>
          <div class="video-info">
            <h4 class="video-title">{{ video.title }}</h4>
            <p class="channel-name">{{ video.channel.title }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- No results state -->
    <div v-if="!loading && videos.length === 0 && currentQuery" class="no-results">
      No videos found for "{{ currentQuery }}"
    </div>
    
    <!-- Selected video details -->
    <div v-if="selectedVideo" class="selected-video-details">
      <h3>Selected Video</h3>
      <h4>{{ selectedVideo.title }}</h4>
      <div v-if="transcript.length > 0" class="transcript-preview">
        <h5>Transcript Preview</h5>
        <div class="transcript-container">
          <p v-for="(segment, index) in transcript.slice(0, 5)" :key="index" class="transcript-segment">
            <span class="transcript-time">{{ formatTime(segment.start) }}</span>
            {{ segment.text }}
          </p>
          <p v-if="transcript.length > 5" class="transcript-more">
            ... and {{ transcript.length - 5 }} more segments
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { vueComposables } from '../../../graphql';

const { useYouTubeSearch, useYouTubeVideo } = vueComposables;

export default {
  name: 'YouTubeSearch',
  props: {
    initialQuery: {
      type: String,
      default: ''
    }
  },
  emits: ['video-select'],
  setup(props, { emit }) {
    // Reactive state
    const searchTerm = ref('');
    const currentQuery = ref('');
    const selectedVideoId = ref(null);
    
    // Use our GraphQL composables
    const { 
      videos, 
      loading, 
      error, 
      search 
    } = useYouTubeSearch();
    
    const { 
      video: selectedVideo, 
      transcript, 
      loading: videoLoading 
    } = useYouTubeVideo(selectedVideoId);
    
    // Methods
    const handleSubmit = () => {
      currentQuery.value = searchTerm.value;
      search(searchTerm.value);
    };
    
    const handleVideoSelect = (video) => {
      selectedVideoId.value = video.id;
      emit('video-select', video);
    };
    
    const formatTime = (seconds) => {
      const min = Math.floor(seconds / 60);
      const sec = Math.floor(seconds % 60);
      return `${min}:${sec.toString().padStart(2, '0')}`;
    };
    
    // Watch for selected video and transcript changes
    watch([selectedVideo, transcript], ([newVideo, newTranscript]) => {
      if (newVideo && newTranscript) {
        emit('video-select', {
          ...newVideo,
          transcript: newTranscript
        });
      }
    });
    
    // If initial query is provided, search on mount
    onMounted(() => {
      if (props.initialQuery) {
        searchTerm.value = props.initialQuery;
        handleSubmit();
      }
    });
    
    return {
      searchTerm,
      currentQuery,
      selectedVideoId,
      videos,
      loading,
      error,
      selectedVideo,
      transcript,
      videoLoading,
      handleSubmit,
      handleVideoSelect,
      formatTime
    };
  }
};
</script>

<style scoped>
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
  background-color: #2196F3;
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
  border: 2px solid #2196F3;
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

.selected-video-details {
  margin-top: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.transcript-preview {
  margin-top: 15px;
}

.transcript-container {
  max-height: 200px;
  overflow-y: auto;
  background-color: white;
  border-radius: 4px;
  padding: 10px;
  border: 1px solid #ddd;
}

.transcript-segment {
  margin: 5px 0;
  font-size: 14px;
  line-height: 1.4;
}

.transcript-time {
  color: #2196F3;
  font-weight: bold;
  margin-right: 10px;
}

.transcript-more {
  text-align: center;
  font-style: italic;
  color: #757575;
}
</style> 