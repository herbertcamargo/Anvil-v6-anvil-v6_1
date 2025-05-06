# GraphQL Integration for Anvil

This module provides GraphQL functionality for more efficient API communication with YouTube endpoints, allowing you to fetch only the specific data your components need.

## Overview

GraphQL offers several advantages over traditional REST API calls:

1. **Precise Data Fetching**: Only request exactly what you need, reducing over-fetching and under-fetching
2. **Reduced Network Traffic**: Fewer API calls by combining multiple data needs in a single query
3. **Strongly Typed Schema**: Clear contract between client and server for reliable integration
4. **Efficient Caching**: Better client-side caching opportunities due to consistent data shape

## Architecture

This implementation uses a custom Apollo Client setup adapted for Anvil's architecture:

```
graphql/
├── schema.js           # GraphQL schema definition
├── resolvers.js        # Resolvers that map to Anvil server functions
├── client.js           # Apollo Client implementation with query definitions
├── hooks.js            # React hooks for using GraphQL
├── vue-composables.js  # Vue composition API for using GraphQL
└── index.js            # Main exports
```

## Integration with YouTube API

Our GraphQL implementation provides efficient access to YouTube data through:

- Video search queries
- Video details requests
- Transcript retrieval
- Combined video details + transcript queries

All while only fetching exactly the fields your components need.

## Usage with React

```jsx
import { reactHooks } from '../../graphql';

const { useYouTubeSearch, useYouTubeVideo } = reactHooks;

function MyComponent() {
  // Search for videos
  const { videos, loading, error, search } = useYouTubeSearch();
  
  // Get video details with transcript
  const { video, transcript } = useYouTubeVideo('abc123');
  
  // Event handler for search form
  const handleSearch = (query) => {
    search(query);
  };
  
  return (
    <div>
      {/* Component UI */}
    </div>
  );
}
```

## Usage with Vue

```vue
<script>
import { vueComposables } from '../../graphql';

export default {
  setup() {
    const videoId = ref('abc123');
    
    // Search for videos
    const { videos, loading, error, search } = vueComposables.useYouTubeSearch();
    
    // Get video details with transcript
    const { video, transcript } = vueComposables.useYouTubeVideo(videoId);
    
    // Event handler for search form
    const handleSearch = (query) => {
      search(query);
    };
    
    return {
      videos,
      loading,
      error,
      search,
      video,
      transcript,
      handleSearch
    };
  }
}
</script>
```

## Available Queries

The following GraphQL queries are available:

### Video Search

```graphql
query SearchVideos($query: String!, $maxResults: Int) {
  searchVideos(query: $query, maxResults: $maxResults) {
    id
    title
    description
    thumbnail_url
    published
    channel {
      id
      title
    }
  }
}
```

### Video Details

```graphql
query GetVideo($id: ID!) {
  video(id: $id) {
    id
    snippet {
      title
      description
      publishedAt
      thumbnails {
        high { url }
      }
      channelTitle
    }
    statistics {
      viewCount
      likeCount
      commentCount
    }
    contentDetails {
      duration
    }
  }
}
```

### Video with Transcript

```graphql
query GetVideoWithTranscript($id: ID!) {
  videoWithTranscript(id: $id) {
    id
    snippet {
      title
      description
    }
    transcript {
      text
      start
      duration
    }
  }
}
```

## Benefits Over Direct API Calls

1. **Reduced Data Transfer**: Only request fields you need instead of receiving entire API responses
2. **Fewer HTTP Requests**: Combine multiple API calls into a single GraphQL query
3. **Consistent Error Handling**: Standardized error handling across all API interactions
4. **Improved Developer Experience**: Type-safe queries with proper tooling and intellisense
5. **Optimized Caching**: More efficient caching through Apollo Client's normalized cache

## Performance Considerations

- The GraphQL layer adds minimal overhead compared to direct API calls
- Benefits from data selection usually outweigh any added complexity
- Apollo Client's caching further reduces unnecessary network requests

## Extending

To add more queries or data sources:

1. Update the schema in `schema.js`
2. Add new resolvers in `resolvers.js`
3. Define new queries in `client.js`
4. Create convenience hooks/composables as needed 