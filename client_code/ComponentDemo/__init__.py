import anvil
from anvil import *
import anvil.server
import anvil.js
from anvil.js.window import document

class ComponentDemo(anvil.Component):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def form_show(self, **event_args):
    """This method is called when the form is shown on the screen"""
    # We need to load our compiled React and Vue component scripts for TodoList
    anvil.js.call_js('eval', """
      if (!window.reactComponentsLoaded) {
        var script = document.createElement('script');
        script.src = '_/theme/components/reactComponents.js';
        script.onload = function() {
          window.reactComponentsLoaded = true;
          if (typeof window.renderReactComponent === 'function') {
            window.renderReactComponent('TodoList', 'react-container');
            // Also render WebAssembly video processor component
            window.renderReactComponent('VideoProcessor', 'react-video-processor');
          }
        };
        document.head.appendChild(script);
      } else if (typeof window.renderReactComponent === 'function') {
        window.renderReactComponent('TodoList', 'react-container');
        window.renderReactComponent('VideoProcessor', 'react-video-processor');
      }
      
      if (!window.vueComponentsLoaded) {
        var script = document.createElement('script');
        script.src = '_/theme/components/vueComponents.js';
        script.onload = function() {
          window.vueComponentsLoaded = true;
          if (typeof window.renderVueComponent === 'function') {
            window.renderVueComponent('TodoList', 'vue-container');
            // Also render WebAssembly video processor component
            window.renderVueComponent('VideoProcessor', 'vue-video-processor');
          }
        };
        document.head.appendChild(script);
      } else if (typeof window.renderVueComponent === 'function') {
        window.renderVueComponent('TodoList', 'vue-container');
        window.renderVueComponent('VideoProcessor', 'vue-video-processor');
      }
    """) 