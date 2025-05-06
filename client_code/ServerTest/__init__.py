from ._anvil_designer import ServerTestTemplate
from anvil import *
import anvil.server
from ..html_top_bar.YouTubeGrid import YouTubeGrid
from ..html_top_bar.YouTubePlayer import YouTubePlayer

class ServerTest(ServerTestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Set up YouTube components
    self.setup_youtube_components()
    
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
      
  def setup_youtube_components(self):
    """Set up YouTube related components"""
    # Create YouTube grid component
    self.youtube_grid = YouTubeGrid()
    self.yt_grid_container.add_component(self.youtube_grid)
    
    # Create YouTube player component
    self.youtube_player = YouTubePlayer()
    self.yt_player_container.add_component(self.youtube_player)
    
    # Set up video selection handler
    def handle_video_selected(video):
      self.youtube_player.play_video(video)
      # Scroll to player
      self.yt_player_container.scroll_into_view()
    
    # Assign the handler to the grid
    self.youtube_grid.video_selected = handle_video_selected
      
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
    self.youtube_grid.update_videos(videos)
    
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