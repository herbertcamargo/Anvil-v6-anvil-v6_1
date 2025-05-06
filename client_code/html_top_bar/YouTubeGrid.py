from ._anvil_designer import YouTubeGridTemplate
from anvil import *
import anvil.js

class YouTubeGrid(YouTubeGridTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Initialize videos list
    self.videos = []
    
  def setup_js_handlers(self):
    """Set up click handlers for the video thumbnails"""
    grid_container = anvil.js.get_dom_node(self).querySelector('.yt-grid-container')
    if grid_container:
      # Add click event listeners to all thumbnail containers
      thumbnails = grid_container.querySelectorAll('.thumbnail-container')
      for i, thumbnail in enumerate(thumbnails):
        # Use a closure to capture the current index
        def create_click_handler(index):
          return lambda event: self.thumbnail_click(index)
        
        thumbnail.addEventListener('click', create_click_handler(i))
  
  def update_videos(self, videos_data):
    """Update the grid with new video data
    
    Args:
        videos_data: List of dicts with video info (id, title, thumbnail_url)
    """
    self.videos = videos_data
    
    # Get the HTML container
    grid_container = anvil.js.get_dom_node(self).querySelector('.yt-grid-container')
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
      
      # Create thumbnail image
      img = anvil.js.window.document.createElement('img')
      img.src = video.get('thumbnail_url', 'https://via.placeholder.com/320x180')
      img.alt = video.get('title', 'Video thumbnail')
      img.className = 'thumbnail-image'
      
      # Create title element
      title = anvil.js.window.document.createElement('p')
      title.className = 'video-title'
      title.textContent = video.get('title', 'Untitled video')
      
      # Append elements to container
      thumbnail_div.appendChild(img)
      thumbnail_div.appendChild(title)
      grid_container.appendChild(thumbnail_div)
    
    # Set up click handlers
    self.setup_js_handlers()
  
  def thumbnail_click(self, index):
    """Handle thumbnail click event
    
    Args:
        index: Index of the clicked video in the videos list
    """
    if index < len(self.videos):
      video = self.videos[index]
      # Call the custom event handler if it exists
      if hasattr(self, 'video_selected') and callable(self.video_selected):
        self.video_selected(video) 