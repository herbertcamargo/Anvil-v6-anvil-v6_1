from ._anvil_designer import ServerTestTemplate
from anvil import *
import anvil.server
import anvil.js

class ServerTest(ServerTestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Set up YouTube functionality
    self.setup_youtube_functionality()
    
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
      
  def setup_youtube_functionality(self):
    """Set up YouTube functionality directly in the form"""
    self.videos = []
    
    # Set up click handler for the grid
    self.yt_grid_container.tag.html = """
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
    self.yt_player_container.tag.html = """
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
    
  def update_youtube_grid(self, videos_data):
    """Update the grid with new video data"""
    self.videos = videos_data
    
    # Get the HTML container
    grid_container = anvil.js.get_dom_node(self.yt_grid_container).querySelector('.yt-grid-container')
    if not grid_container:
      return
      
    # Clear existing content
    grid_container.innerHTML = ''
    
    # Add new thumbnails (up to 12)
    for i, video in enumerate(videos_data[:12]):
      # Create thumbnail container
      thumbnail_div = anvil.js.window.document.createElement('div')
      thumbnail_div.className = 'thumbnail-container'
      thumbnail_div.setAttribute('data-video-id', video.get('id', ''))
      thumbnail_div.setAttribute('data-index', str(i))
      
      # Create thumbnail image
      img = anvil.js.window.document.createElement('img')
      img.src = video.get('thumbnail_url', 'https://via.placeholder.com/320x180')
      img.alt = video.get('title', 'Video thumbnail')
      img.className = 'thumbnail-image'
      
      # Create title element
      title = anvil.js.window.document.createElement('p')
      title.className = 'video-title'
      title.textContent = video.get('title', 'Untitled video')
      
      # Add click event
      thumbnail_div.addEventListener('click', self.create_thumbnail_click_handler(i))
      
      # Append elements to container
      thumbnail_div.appendChild(img)
      thumbnail_div.appendChild(title)
      grid_container.appendChild(thumbnail_div)
      
  def create_thumbnail_click_handler(self, index):
    """Create a click handler for a thumbnail at the specified index"""
    def handler(event):
      if index < len(self.videos):
        self.play_video(self.videos[index])
    return handler
    
  def play_video(self, video_data):
    """Play the specified video"""
    video_id = video_data.get('id')
    if not video_id:
      return
      
    # Update the iframe src with the new video ID
    player_container = anvil.js.get_dom_node(self.yt_player_container).querySelector('.youtube-player-container')
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
    title_element = anvil.js.get_dom_node(self.yt_player_container).querySelector('.video-title-display')
    if title_element and video_data.get('title'):
      title_element.textContent = video_data.get('title')
      
    # Scroll to player
    self.yt_player_container.scroll_into_view()
      
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
      videos = anvil.server.call('search_youtube', query)
      self.search_status.text = "Search completed via server!"
      self.search_status.foreground = "#4CAF50"  # Green color
      
    except Exception as e:
      # Fall back to client-side mock data if server function fails
      self.search_status.text = f"Server search failed, using mock data: {str(e)}"
      self.search_status.foreground = "#FF9800"  # Orange color
      
      # Create mock YouTube results
      videos = [
        {
          'id': 'dQw4w9WgXcQ',
          'title': f'Mock YouTube Result 1 for: {query}',
          'thumbnail_url': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
        },
        {
          'id': 'QvKBP1PbSjE',
          'title': f'Mock YouTube Result 2 for: {query}',
          'thumbnail_url': 'https://i.ytimg.com/vi/QvKBP1PbSjE/mqdefault.jpg',
        },
        {
          'id': 'G1IbRujko-A',
          'title': f'Mock YouTube Result 3 for: {query}',
          'thumbnail_url': 'https://i.ytimg.com/vi/G1IbRujko-A/mqdefault.jpg',
        },
        {
          'id': '7PJA0p-kzOo',
          'title': f'Mock YouTube Result 4 for: {query}',
          'thumbnail_url': 'https://i.ytimg.com/vi/7PJA0p-kzOo/mqdefault.jpg',
        },
        {
          'id': 'KpOtuoHL45Y',
          'title': f'Mock YouTube Result 5 for: {query}',
          'thumbnail_url': 'https://i.ytimg.com/vi/KpOtuoHL45Y/mqdefault.jpg',
        },
        {
          'id': 'OPf0YbXqDm0',
          'title': f'Mock YouTube Result 6 for: {query}',
          'thumbnail_url': 'https://i.ytimg.com/vi/OPf0YbXqDm0/mqdefault.jpg',
        },
        {
          'id': 'J--0d3tFTI4',
          'title': f'Mock YouTube Result 7 for: {query}',
          'thumbnail_url': 'https://i.ytimg.com/vi/J--0d3tFTI4/mqdefault.jpg',
        },
        {
          'id': '2vjPBrBU-TM',
          'title': f'Mock YouTube Result 8 for: {query}',
          'thumbnail_url': 'https://i.ytimg.com/vi/2vjPBrBU-TM/mqdefault.jpg',
        },
        {
          'id': '09R8_2nJtjg',
          'title': f'Mock YouTube Result 9 for: {query}',
          'thumbnail_url': 'https://i.ytimg.com/vi/09R8_2nJtjg/mqdefault.jpg',
        }
      ]
    
    # Update the YouTube grid with videos
    self.update_youtube_grid(videos)
    
    # Show a notification
    Notification(f"Found {len(videos)} YouTube videos for '{query}'", timeout=3).show()
    
    # Scroll to see results
    self.yt_grid_container.scroll_into_view()
      
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