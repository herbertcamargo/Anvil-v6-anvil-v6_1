// GraphQL main exports for Anvil application
import client, { executeQuery, executeMutation, Queries } from './client';
import * as reactHooks from './hooks';
import * as vueComposables from './vue-composables';

// Export everything for easy importing
export {
  // Apollo client
  client,
  
  // Utility functions
  executeQuery,
  executeMutation,
  
  // GraphQL queries
  Queries,
  
  // React hooks
  reactHooks,
  
  // Vue composables
  vueComposables
};

// Default export
export default {
  client,
  executeQuery,
  executeMutation,
  Queries,
  reactHooks,
  vueComposables
}; 