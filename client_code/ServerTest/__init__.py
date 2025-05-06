from ._anvil_designer import ServerTestTemplate
from anvil import *
import anvil.server
import anvil.js
from anvil.js.window import HTMLElement

class ServerTest(ServerTestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Enable global exception reporting for all JavaScript callbacks
    anvil.js.report_all_exceptions(True)
    
    # Add global placeholder image handler
    self.add_placeholder_image_handler()
    
    # Set up YouTube functionality
    self.setup_youtube_functionality()
    
    # Add debug functions
    self.debug_panel = FlowPanel()
    self.debug_button = Button(text="Debug HTML", role="outlined-button")
    self.debug_button.set_event_handler('click', self.debug_html)
    self.debug_panel.add_component(self.debug_button)
    
    # Add test grid button
    self.test_grid_button = Button(text="Create Test Grid", role="primary-color")
    self.test_grid_button.set_event_handler('click', self.create_test_grid)
    self.debug_panel.add_component(self.test_grid_button)
    
    # Add the debug panel 
    self.add_component(self.debug_panel, index=4)  # Place it after the search section heading
    
    # Try to call server functions to see if they work
    try:
      # Try to call test function
      self.result_label.text = "Testing server functions..."
      result = anvil.server.call('hello')
      self.result_label.text = f"Server Response: {result}"
      self.status_label.text = "Server functions are working!"
      self.status_label.foreground = "#4CAF50"  # Green color
    except Exception as e:
      # Show error if server functions don't work
      self.result_label.text = f"Error: {str(e)}"
      self.status_label.text = "Server functions are NOT working!"
      self.status_label.foreground = "#F44336"  # Red color
      
  def add_placeholder_image_handler(self):
    """Add a global handler to replace all placeholder.com images with data URIs"""
    # Create small avatar placeholder (40x40)
    avatar_placeholder = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' fill='%23cccccc'/%3E%3Ctext x='50%25' y='50%25' font-family='Arial' font-size='10' text-anchor='middle' fill='%23666666'%3E?%3C/text%3E%3C/svg%3E"
    
    # Create a global script to intercept ALL network requests to placeholder.com
    placeholder_script = anvil.js.window.document.createElement('script')
    placeholder_script.innerHTML = f"""
    (function() {{
      // Block ALL placeholder.com requests at the fetch/XHR level
      const originalFetch = window.fetch;
      window.fetch = function(url, options) {{
        if (url && url.toString().includes('placeholder.com')) {{
          console.log('Blocked fetch request to placeholder.com:', url);
          return Promise.resolve(new Response(
            new Blob([''], {{type: 'text/plain'}}),
            {{status: 200, statusText: 'Blocked by Anvil'}}
          ));
        }}
        return originalFetch.apply(this, arguments);
      }};
      
      // Block XMLHttpRequest as well
      const originalOpen = XMLHttpRequest.prototype.open;
      XMLHttpRequest.prototype.open = function(method, url, ...args) {{
        if (url && url.toString().includes('placeholder.com')) {{
          console.log('Blocked XHR request to placeholder.com:', url);
          this.abort();
          return;
        }}
        return originalOpen.apply(this, [method, url, ...args]);
      }};
      
      // Create data URIs for different image sizes
      const generatePlaceholder = (width, height) => {{
        if (width <= 40 && height <= 40) {{
          return "{avatar_placeholder}";
        }} else {{
          return `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='${{width}}' height='${{height}}' viewBox='0 0 ${{width}} ${{height}}'%3E%3Crect width='${{width}}' height='${{height}}' fill='%23cccccc'/%3E%3Ctext x='50%25' y='50%25' font-family='Arial' font-size='${{Math.max(12, Math.min(24, width/10))}}' text-anchor='middle' fill='%23666666'%3E${{width}}x${{height}}%3C/text%3E%3C/svg%3E`;
        }}
      }};
      
      // Block and replace image sources at the DOM level
      function replaceImgSrc(img) {{
        if (img.src && img.src.includes('placeholder.com')) {{
          // Extract dimensions from URL if possible
          const match = img.src.match(/placeholder\\.com\\/(\\d+)x(\\d+)/);
          const width = match ? parseInt(match[1]) : 40;
          const height = match ? parseInt(match[2]) : 40;
          
          // Replace with appropriate SVG
          img.src = generatePlaceholder(width, height);
          
          // Prevent further loading attempts
          img.setAttribute('data-original-src', 'blocked-placeholder');
        }}
      }}
      
      // Process all existing images
      document.querySelectorAll('img').forEach(replaceImgSrc);
      
      // Watch for dynamically added images
      const observer = new MutationObserver(mutations => {{
        mutations.forEach(mutation => {{
          if (mutation.addedNodes) {{
            mutation.addedNodes.forEach(node => {{
              // Process the node itself if it's an image
              if (node.nodeName === 'IMG') replaceImgSrc(node);
              
              // Process any images inside the node
              if (node.querySelectorAll) {{
                node.querySelectorAll('img').forEach(replaceImgSrc);
              }}
            }});
          }}
          
          // Also check for changed src attributes
          if (mutation.type === 'attributes' && 
              mutation.attributeName === 'src' && 
              mutation.target.nodeName === 'IMG') {{
            replaceImgSrc(mutation.target);
          }}
        }});
      }});
      
      // Observe the entire document for changes
      observer.observe(document.documentElement, {{ 
        childList: true, 
        subtree: true,
        attributes: true,
        attributeFilter: ['src']
      }});
      
      // Block and prevent any access to placeholder.com at the lowest level
      // by defining a service worker that blocks those requests
      if ('serviceWorker' in navigator) {{
        navigator.serviceWorker.getRegistrations().then(registrations => {{
          for (let registration of registrations) {{
            if (registration.scope.includes(window.location.origin)) {{
              registration.unregister();
            }}
          }}
        }});
      }}
      
      console.log('Placeholder image blocking system initialized');
    }})();
    """
    
    # Add the script to the document head
    anvil.js.window.document.head.appendChild(placeholder_script)
    
  def create_test_grid(self, **event_args):
    """Create a test grid with simple colored boxes"""
    test_videos = []
    
    # Create 9 test videos with different colors
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'teal', 'pink', 'brown', 'gray']
    
    for i, color in enumerate(colors):
      test_videos.append({
        'id': f'test-{i}',
        'title': f'Test Video {i+1} ({color})',
        'thumbnail_url': f'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" style="background:{color}"><text x="50%" y="50%" fill="white" font-size="20" text-anchor="middle">Test {i+1}</text></svg>'
      })
    
    # Update the grid with these test videos
    self.update_youtube_grid(test_videos)
    
    # Scroll to the grid container
    self.yt_grid_container.scroll_into_view()
    
  def debug_html(self, **event_args):
    """Debug HTML structure and components"""
    try:
      # Check if HTML components exist
      html_status = "HTML components:\n"
      html_status += f"Grid HTML exists: {hasattr(self, 'grid_html')}\n"
      html_status += f"Player HTML exists: {hasattr(self, 'player_html')}\n"
      
      # Check containers
      container_status = "Containers:\n"
      container_status += f"Grid container exists: {self.yt_grid_container is not None}\n"
      container_status += f"Player container exists: {self.yt_player_container is not None}\n"
      
      # Check DOM elements
      dom_status = "DOM elements:\n"
      grid_container = None
      player_container = None
      
      try:
        grid_container = anvil.js.get_dom_node(self.grid_html).querySelector('.yt-grid-container')
        dom_status += f"Grid container DOM element exists: {grid_container is not None}\n"
      except:
        dom_status += "Error accessing grid container DOM element\n"
        
      try:
        player_container = anvil.js.get_dom_node(self.player_html).querySelector('.youtube-player-container')
        dom_status += f"Player container DOM element exists: {player_container is not None}\n"
      except:
        dom_status += "Error accessing player container DOM element\n"
        
      # Show complete status
      alert(f"{html_status}\n{container_status}\n{dom_status}")
      
      # Try to add a test thumbnail
      if grid_container:
        grid_container.innerHTML = '<div style="background-color: red; color: white; padding: 20px; margin: 10px;">Test Thumbnail</div>'
        alert("Added test thumbnail - check if it's visible")
      
    except Exception as e:
      alert(f"Debug error: {str(e)}")
      
  def setup_youtube_functionality(self):
    """Set up YouTube functionality directly in the form"""
    self.videos = []
    
    # Create HTML components for grid and player
    self.yt_grid_container.clear()
    self.grid_html = HtmlPanel()
    self.yt_grid_container.add_component(self.grid_html)
    self.grid_html.html = """
    <style>
      .yt-grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 20px;
        padding: 20px;
        width: 100%;
      }
      
      .thumbnail-container {
        display: flex;
        flex-direction: column;
        cursor: pointer;
        transition: transform 0.2s;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        background-color: white;
      }
      
      .thumbnail-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
      }
      
      .thumbnail-image {
        width: 100%;
        aspect-ratio: 16/9;
        object-fit: cover;
      }
      
      .video-title {
        padding: 10px;
        margin: 0;
        font-size: 14px;
        font-weight: 500;
        height: 3em;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
      }
    </style>
    
    <div class="yt-grid-container">
      <!-- Video thumbnails will be inserted here dynamically -->
    </div>
    """
    
    # Set up player container
    self.yt_player_container.clear()
    self.player_html = HtmlPanel()
    self.yt_player_container.add_component(self.player_html)
    self.player_html.html = """
    <style>
      .youtube-player-wrapper {
        display: flex;
        flex-direction: column;
        width: 100%;
      }
      
      .video-title-display {
        font-size: 18px;
        font-weight: 600;
        margin: 10px 0;
        padding: 0 10px;
      }
      
      .youtube-player-container {
        position: relative;
        width: 100%;
        padding-bottom: 56.25%; /* 16:9 aspect ratio */
        height: 0;
        overflow: hidden;
        border-radius: 8px;
      }
      
      .youtube-iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 8px;
      }
    </style>
    
    <div class="youtube-player-wrapper">
      <h2 class="video-title-display">Select a video to play</h2>
      <div class="youtube-player-container">
        <!-- YouTube iframe will be inserted here dynamically -->
      </div>
    </div>
    """
    
    # Add headings to make the sections clearer
    self.yt_grid_container.add_component(Label(text="YouTube Video Results", role="heading"), index=0)
    self.yt_player_container.add_component(Label(text="Video Player", role="heading"), index=0)
    
  def update_youtube_grid(self, videos_data):
    """Update the grid with new video data"""
    self.videos = videos_data
    
    # Get the HTML container
    grid_container = anvil.js.get_dom_node(self.grid_html).querySelector('.yt-grid-container')
    if not grid_container:
      print("Error: Could not find grid container")
      alert("Could not find grid container")
      return
      
    # Clear existing content
    grid_container.innerHTML = ''
    
    # Check if we have videos to display
    if not videos_data:
      # Display a "no videos found" message in the grid
      grid_container.innerHTML = """
        <div style="text-align: center; padding: 40px; width: 100%;">
          <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 30px; background-color: #f8f9fa; display: inline-block; max-width: 600px;">
            <h3 style="color: #6c757d; margin-bottom: 15px;">No Videos Found</h3>
            <p style="color: #6c757d;">Enter a search term and connect to the YouTube API to display real video results.</p>
            <p style="color: #6c757d; font-size: 0.9em; margin-top: 15px;">This application does not display pre-loaded dummy videos.</p>
          </div>
        </div>
      """
      return
    
    # Otherwise, continue with normal video display (if we have videos)
    thumbnails_html = ""
    
    # Data URI for default thumbnail (gray background with text)
    default_thumbnail = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='320' height='180' viewBox='0 0 320 180'%3E%3Crect width='320' height='180' fill='%23cccccc'/%3E%3Ctext x='50%25' y='50%25' font-family='Arial' font-size='24' text-anchor='middle' fill='%23666666'%3ENo Thumbnail%3C/text%3E%3C/svg%3E"
    
    for i, video in enumerate(videos_data[:12]):
      video_id = video.get('id', '')
      title = video.get('title', 'Untitled video')
      # Use the provided thumbnail URL or the default if it's a placeholder or missing
      thumbnail_url = video.get('thumbnail_url', default_thumbnail)
      if "placeholder.com" in thumbnail_url:
        thumbnail_url = default_thumbnail
      
      # Create the thumbnail HTML with a data attribute for the index
      thumbnails_html += f"""
        <div class="thumbnail-container" data-index="{i}" data-video-id="{video_id}" onclick="handleThumbnailClick({i})">
          <img src="{thumbnail_url}" alt="{title}" class="thumbnail-image" onerror="this.onerror=null; this.src='{default_thumbnail}'">
          <p class="video-title">{title}</p>
        </div>
      """
    
    # First, inject the click handler function into the page
    # Use a separate module-like IIFE (Immediately Invoked Function Expression) for better scoping
    click_handler_script = anvil.js.window.document.createElement('script')
    click_handler_script.innerHTML = """
      (function() {
        // Create a proper module-like scope for YouTube thumbnail handlers
        window.handleThumbnailClick = function(index) {
          var event = new CustomEvent('thumbnail-click', { 
            detail: { index: index },
            bubbles: true, 
            cancelable: true 
          });
          document.dispatchEvent(event);
        };
        
        // Export video player functionality to global scope
        window.YouTubePlayer = {
          loadVideo: function(videoId, title) {
            // This method could be called directly from JavaScript if needed
            return new Promise(function(resolve, reject) {
              try {
                // Implementation could be expanded later
                console.log("Loading video: " + videoId + " - " + title);
                resolve({videoId: videoId, title: title});
              } catch (error) {
                reject(error);
              }
            });
          }
        };
      })();
    """
    anvil.js.window.document.head.appendChild(click_handler_script)
    
    # Set all thumbnails at once
    grid_container.innerHTML = thumbnails_html
    
    # Only add event listeners if we have videos
    if videos_data:
      # Add a document-level event listener for the custom event
      @anvil.js.report_exceptions
      def handle_thumbnail_event(e):
        index = e.detail.index
        self.thumbnail_click(dict(index=index))
      
      # Store the event listener function to be able to remove it later if needed
      self._thumbnail_handler = handle_thumbnail_event
      
      # Add the event listener to the document
      anvil.js.window.document.addEventListener('thumbnail-click', self._thumbnail_handler)
      
  def thumbnail_click(self, *args, **event_args):
    """Handle thumbnail click from HTML"""
    index = event_args.get('index', 0)
    alert(f"Thumbnail clicked: {index}")
    if 0 <= index < len(self.videos):
      self.play_video(self.videos[index])
    
  def play_video(self, video_data):
    """Play the specified video"""
    video_id = video_data.get('id')
    if not video_id:
      return
      
    title = video_data.get('title', 'Untitled video')
      
    try:
      # Call our JavaScript player function and await the promise
      result = anvil.js.await_promise(
        anvil.js.window.YouTubePlayer.loadVideo(video_id, title)
      )
      
      # Now update the iframe src with the new video ID
      player_container = anvil.js.get_dom_node(self.player_html).querySelector('.youtube-player-container')
      if player_container:
        player_container.innerHTML = f"""
          <iframe 
            src="https://www.youtube.com/embed/{video_id}?autoplay=1" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen
            class="youtube-iframe">
          </iframe>
        """
        
      # Update video title if available
      title_element = anvil.js.get_dom_node(self.player_html).querySelector('.video-title-display')
      if title_element and title:
        title_element.textContent = title
        
      # Scroll to player
      self.yt_player_container.scroll_into_view()
      
    except anvil.js.ExternalError as js_error:
      # Handle JavaScript errors properly
      error_message = str(js_error.original_error) if hasattr(js_error, 'original_error') else str(js_error)
      alert(f"Error loading video: {error_message}")
      print(f"JavaScript error: {error_message}")
    
  def search_button_click(self, **event_args):
    """Handle YouTube search with server function fallback"""
    query = self.search_box.text
    if not query:
      alert("Please enter a search term")
      return
      
    self.search_status.text = "Searching..."
    self.search_status.foreground = "#2196F3"  # Blue color
    
    try:
      # Try to call server function for search
      self.search_status.text = "Trying server search..."
      
      try:
        # Attempt to call the real YouTube API through server function
        videos = anvil.server.call('search_youtube', query)
        
        if videos and len(videos) > 0:
          self.search_status.text = f"Found {len(videos)} videos via YouTube API!"
          self.search_status.foreground = "#4CAF50"  # Green color
          
          # Create a separate notification showing we're updating thumbnails
          Notification("Loading thumbnails from YouTube API...", timeout=2).show()
          
          # Update the YouTube grid with API results
          self.update_youtube_grid(videos)
          
          # Show a notification of success
          Notification(f"Successfully added {len(videos)} videos to grid", timeout=3).show()
        else:
          # No videos found from the API
          self.search_status.text = f"No videos found for '{query}' via YouTube API"
          self.search_status.foreground = "#FF9800"  # Orange color
          
          # Update with empty grid
          self.update_youtube_grid([])
          
          # Show notification
          Notification("No videos found for your search", timeout=3).show()
          
      except Exception as server_error:
        # API call failed - show the error but don't use dummy data
        self.search_status.text = f"YouTube API error: {str(server_error)}"
        self.search_status.foreground = "#FF9800"  # Orange color
        
        # Update with empty grid
        self.update_youtube_grid([])
        
        # Show notification about API requirement
        Notification("YouTube API connection required - no dummy data will be shown", timeout=4).show()
      
      # Scroll to see results
      self.yt_grid_container.scroll_into_view()
      
    except Exception as e:
      # Show error notification if search completely fails
      self.search_status.text = f"Search failed: {str(e)}"
      self.search_status.foreground = "#F44336"  # Red color
      alert(f"Error during search: {str(e)}")
      print(f"Search error: {str(e)}")
    
  def back_home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('MinimalApp')

  def test_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      self.result_label.text = "Testing server connection..."
      result = anvil.server.call('minimal_test')
      
      # Format the result nicely
      if isinstance(result, dict):
        result_text = f"Status: {result.get('status', 'unknown')}\n"
        for key, value in result.items():
          if key != 'status':
            result_text += f"{key}: {value}\n"
        self.result_label.text = result_text
      else:
        self.result_label.text = f"Server test result: {result}"
        
      self.result_label.foreground = "#00aa00"  # Green for success
    except Exception as e:
      self.result_label.text = f"Error: {str(e)}"
      self.result_label.foreground = "#aa0000"  # Red for error
      
  def advanced_test_button_click(self, **event_args):
    """This method is called when the advanced test button is clicked"""
    try:
      self.result_label.text = "Pinging server..."
      # Try the simplest possible server call without any imports
      ping_result = anvil.server.call('ping')
      self.result_label.text = f"Ping result: {ping_result}"
      self.result_label.foreground = "#00aa00"  # Green for success
    except Exception as e:
      self.result_label.text = f"Ping error: {str(e)}"
      self.result_label.foreground = "#aa0000"  # Red for error 

  def return_to_main_app(self, **event_args):
    """Return to the main application"""
    try:
      self.result_label.text = "Opening minimal app..."
      open_form('MinimalApp')
    except Exception as e:
      self.result_label.text = f"Error opening minimal app: {str(e)}"
      self.result_label.foreground = "#aa0000"  # Red for error 