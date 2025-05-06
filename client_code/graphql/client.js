// GraphQL client implementation for Anvil
import { ApolloClient, InMemoryCache, ApolloLink, HttpLink } from '@apollo/client';
import { onError } from '@apollo/client/link/error';
import typeDefs from './schema';
import resolvers from './resolvers';

// Create a custom Apollo Link that uses Anvil's server call mechanism instead of HTTP
class AnvilLink extends ApolloLink {
  constructor() {
    super();
  }
  
  request(operation) {
    return new Observable(observer => {
      const { query, variables } = operation;
      
      // Convert GraphQL operation to a format that can be handled by our resolver
      const queryName = query.definitions[0].selectionSet.selections[0].name.value;
      const params = variables || {};
      
      // Use the correct resolver from our resolvers object
      if (resolvers.Query[queryName]) {
        // Call the resolver with empty parent and the variables
        resolvers.Query[queryName](null, params)
          .then(result => {
            // Wrap the result in the format expected by Apollo
            observer.next({
              data: {
                [queryName]: result
              }
            });
            observer.complete();
          })
          .catch(error => {
            observer.error(error);
          });
      } else {
        observer.error(new Error(`No resolver found for query: ${queryName}`));
      }
      
      // Return cleanup function
      return () => {};
    });
  }
}

// Error handling link
const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, locations, path }) => {
      console.error(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
      );
    });
  }
  
  if (networkError) {
    console.error(`[Network error]: ${networkError}`);
  }
});

// Initialize Apollo Client
const client = new ApolloClient({
  link: ApolloLink.from([errorLink, new AnvilLink()]),
  cache: new InMemoryCache(),
  typeDefs,
  resolvers,
});

// Utility function to execute GraphQL queries
export async function executeQuery(query, variables = {}) {
  try {
    const result = await client.query({
      query,
      variables,
      fetchPolicy: 'network-only', // Don't use cache for this
    });
    return result.data;
  } catch (error) {
    console.error('GraphQL query error:', error);
    throw error;
  }
}

// Utility function to execute GraphQL mutations
export async function executeMutation(mutation, variables = {}) {
  try {
    const result = await client.mutate({
      mutation,
      variables,
    });
    return result.data;
  } catch (error) {
    console.error('GraphQL mutation error:', error);
    throw error;
  }
}

// Define common queries
export const Queries = {
  // Query to get video details
  GET_VIDEO: `
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
  `,
  
  // Query to search videos
  SEARCH_VIDEOS: `
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
  `,
  
  // Query to get video with transcript
  GET_VIDEO_WITH_TRANSCRIPT: `
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
  `,
  
  // Query to get just the transcript
  GET_TRANSCRIPT: `
    query GetVideoWithTranscript($id: ID!) {
      videoWithTranscript(id: $id) {
        transcript {
          text
          start
          duration
        }
      }
    }
  `
};

export default client; 