// GraphQL schema for YouTube API integration
const typeDefs = `
  type Channel {
    id: ID!
    title: String
  }

  type Thumbnail {
    url: String
    width: Int
    height: Int
  }

  type Thumbnails {
    default: Thumbnail
    medium: Thumbnail
    high: Thumbnail
    standard: Thumbnail
    maxres: Thumbnail
  }

  type Statistics {
    viewCount: String
    likeCount: String
    dislikeCount: String
    favoriteCount: String
    commentCount: String
  }

  type VideoSnippet {
    publishedAt: String
    channelId: String
    title: String
    description: String
    thumbnails: Thumbnails
    channelTitle: String
    tags: [String]
    categoryId: String
    liveBroadcastContent: String
    defaultAudioLanguage: String
  }

  type ContentDetails {
    duration: String
    dimension: String
    definition: String
    caption: String
    licensedContent: Boolean
    projection: String
  }

  type TranscriptSegment {
    text: String
    start: Float
    duration: Float
  }

  type Video {
    id: ID!
    snippet: VideoSnippet
    statistics: Statistics
    contentDetails: ContentDetails
    transcript: [TranscriptSegment]
  }

  type SearchResult {
    id: ID!
    title: String
    description: String
    thumbnail_url: String
    published: String
    channel: Channel
  }

  type Query {
    video(id: ID!): Video
    searchVideos(query: String!, maxResults: Int): [SearchResult]
    videoWithTranscript(id: ID!): Video
  }
`;

// Export the schema
export default typeDefs; 