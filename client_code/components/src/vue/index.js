import { createApp } from 'vue';
import TodoList from './TodoList.vue';

// Export component classes for individual usage
export { TodoList };

// Function to render a Vue component into a DOM element
export function renderComponent(componentName, containerId, props = {}) {
  const containerElement = document.getElementById(containerId);
  if (!containerElement) {
    console.error(`Element with ID "${containerId}" not found`);
    return;
  }

  const components = {
    TodoList: TodoList
  };

  const Component = components[componentName];
  if (!Component) {
    console.error(`Component "${componentName}" not found`);
    return;
  }

  const app = createApp(Component, props);
  app.mount(containerElement);
  
  // Return the app instance for potential later use
  return app;
}

// Expose the render function globally
window.renderVueComponent = renderComponent; 