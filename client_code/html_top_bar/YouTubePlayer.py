from ._anvil_designer import YouTubePlayerTemplate
from anvil import *
import anvil.js

class YouTubePlayer(YouTubePlayerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Initialize current video ID
    self.current_video_id = None
    
  def play_video(self, video_data):
    """Play the specified video
    
    Args:
        video_data: Dict with video info (id, title, etc.)
    """
    video_id = video_data.get('id')
    if not video_id:
      return
      
    # Update current video ID
    self.current_video_id = video_id
    
    # Update the iframe src with the new video ID
    player_container = anvil.js.get_dom_node(self).querySelector('.youtube-player-container')
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
    title_element = anvil.js.get_dom_node(self).querySelector('.video-title-display')
    if title_element and video_data.get('title'):
      title_element.textContent = video_data.get('title') 