// GraphQL resolvers for YouTube API integration
import anvil from 'anvil-js';

// Resolvers for GraphQL schema
const resolvers = {
  Query: {
    // Resolver for fetching a single video by ID
    video: async (_, { id }) => {
      try {
        // Call Anvil server function to get video details
        const videoDetails = await anvil.server.call('get_video_details', id);
        
        // Convert to GraphQL format
        if (videoDetails) {
          return {
            id: videoDetails.id,
            snippet: {
              publishedAt: videoDetails.published,
              channelId: videoDetails.channel.id,
              title: videoDetails.title,
              description: videoDetails.description,
              thumbnails: {
                default: { url: videoDetails.thumbnail_url },
                medium: { url: videoDetails.thumbnail_url },
                high: { url: videoDetails.thumbnail_url }
              },
              channelTitle: videoDetails.channel.title
            },
            statistics: {
              viewCount: videoDetails.statistics.views,
              likeCount: videoDetails.statistics.likes,
              commentCount: videoDetails.statistics.comments
            },
            contentDetails: {
              duration: videoDetails.duration
            }
          };
        }
        return null;
      } catch (error) {
        console.error('Error in video resolver:', error);
        throw new Error('Failed to fetch video data');
      }
    },
    
    // Resolver for searching videos
    searchVideos: async (_, { query, maxResults = 12 }) => {
      try {
        // Call Anvil server function to search videos
        const videos = await anvil.server.call('search_youtube_videos', query);
        
        // Return in the format expected by our GraphQL schema
        return videos.map(video => ({
          id: video.id,
          title: video.title,
          description: video.description,
          thumbnail_url: video.thumbnail_url,
          published: video.published,
          channel: {
            id: video.channel.id,
            title: video.channel.title
          }
        }));
      } catch (error) {
        console.error('Error in searchVideos resolver:', error);
        throw new Error('Failed to search videos');
      }
    },
    
    // Resolver for fetching video with transcript
    videoWithTranscript: async (_, { id }) => {
      try {
        // Call Anvil server function to get video with transcript
        const result = await anvil.server.call('get_video_with_transcript', id);
        
        if (result) {
          // Convert to GraphQL format
          return {
            id: result.id,
            snippet: {
              publishedAt: result.published,
              channelId: result.channel.id,
              title: result.title,
              description: result.description,
              thumbnails: {
                default: { url: result.thumbnail_url },
                medium: { url: result.thumbnail_url },
                high: { url: result.thumbnail_url }
              },
              channelTitle: result.channel.title
            },
            statistics: {
              viewCount: result.statistics.views,
              likeCount: result.statistics.likes,
              commentCount: result.statistics.comments
            },
            contentDetails: {
              duration: result.duration
            },
            transcript: result.transcript || []
          };
        }
        return null;
      } catch (error) {
        console.error('Error in videoWithTranscript resolver:', error);
        throw new Error('Failed to fetch video with transcript');
      }
    }
  }
};

export default resolvers; 