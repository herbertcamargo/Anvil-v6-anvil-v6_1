import React from 'react';
import ReactDOM from 'react-dom';
import TodoList from './TodoList';
import VideoProcessor from './VideoProcessor';
import YouTubeSearch from './YouTubeSearch';

// Export all components
export {
  VideoProcessor,
  TodoList,
  YouTubeSearch
};

// Function to render a React component into a DOM element
export function renderComponent(componentName, containerId, props = {}) {
  const containerElement = document.getElementById(containerId);
  if (!containerElement) {
    console.error(`Element with ID "${containerId}" not found`);
    return;
  }

  const components = {
    TodoList: TodoList,
    VideoProcessor: VideoProcessor
  };

  const Component = components[componentName];
  if (!Component) {
    console.error(`Component "${componentName}" not found`);
    return;
  }

  ReactDOM.render(
    <Component {...props} />,
    containerElement
  );
}

// Expose the render function globally
window.renderReactComponent = renderComponent; 