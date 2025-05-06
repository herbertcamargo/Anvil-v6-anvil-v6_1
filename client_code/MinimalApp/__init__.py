from ._anvil_designer import MinimalAppTemplate
from anvil import *
from ..html_top_bar.YouTubeGrid import YouTubeGrid
from ..html_top_bar.YouTubePlayer import YouTubePlayer

class MinimalApp(MinimalAppTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Set all panels visible
    self.show_all_panels()
    
    # Initialize YouTube components
    self.setup_youtube_components()
    
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
    
  def show_all_panels(self):
    """Show all panels"""
    self.welcome_panel.visible = True
    self.search_panel.visible = True
    self.compare_panel.visible = True
    
  def home_link_click(self, **event_args):
    """Handle click on Home link - scroll to top"""
    self.welcome_panel.scroll_into_view()
    
  def search_link_click(self, **event_args):
    """Handle click on Search link - scroll to search section"""
    self.search_panel.scroll_into_view()
    
  def comparison_link_click(self, **event_args):
    """Handle click on Comparison link - scroll to comparison section"""
    self.compare_panel.scroll_into_view()
    
  def welcome_search_button_click(self, **event_args):
    """Handle click on Start Searching button - scroll to search section"""
    self.search_panel.scroll_into_view()
    self.search_box.focus()
    
  def welcome_compare_button_click(self, **event_args):
    """Handle click on Practice Comparison button - scroll to comparison section"""
    self.compare_panel.scroll_into_view()
    self.text1_box.focus()
  
  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Use client-side only functionality - no server calls
    query = self.search_box.text
    if not query:
      alert("Please enter a search term")
      return
      
    # Create mock YouTube results without calling the server
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
      },
      {
        'id': 'mWRsgZuwf_8',
        'title': f'Mock YouTube Result 10 for: {query}',
        'thumbnail_url': 'https://i.ytimg.com/vi/mWRsgZuwf_8/mqdefault.jpg',
      },
      {
        'id': 'e-ORhEE9VVg',
        'title': f'Mock YouTube Result 11 for: {query}',
        'thumbnail_url': 'https://i.ytimg.com/vi/e-ORhEE9VVg/mqdefault.jpg',
      },
      {
        'id': 'QcIy9NiNbmo',
        'title': f'Mock YouTube Result 12 for: {query}',
        'thumbnail_url': 'https://i.ytimg.com/vi/QcIy9NiNbmo/mqdefault.jpg',
      }
    ]
    
    # Update the YouTube grid with new videos
    self.youtube_grid.update_videos(videos)
    
    # Show a notification
    Notification(f"Found {len(videos)} YouTube videos for '{query}'", timeout=3).show()
    
    # Scroll to see results
    self.yt_grid_container.scroll_into_view()
    
    # Also show text search results for consistency
    self.results_panel.clear()
    self.results_panel.add_component(Label(text=f"Results for: {query}", role="heading"))
    
    # Add some mock results
    for i in range(3):
      # Create a card for each mock result
      card = ColumnPanel(spacing="medium")
      card.border = "1px solid #ddd"
      # Set padding using spacing property instead of direct padding attribute
      card.spacing = ("medium", "medium", "medium", "medium")
      card.spacing_below = "medium"
      
      # Add mock title and info
      title = Label(text=f"Mock result {i+1} for {query}", role="heading")
      title.bold = True
      info = Label(text="This is a client-side only mock result (no server call)")
      
      card.add_component(title)
      card.add_component(info)
      
      self.results_panel.add_component(card)
    
  def compare_button_click(self, **event_args):
    """Compare texts without server calls"""
    text1 = self.text1_box.text
    text2 = self.text2_box.text
    
    if not text1 or not text2:
      alert("Please enter both texts to compare")
      return
      
    # Simple client-side comparison
    if text1 == text2:
      result = "Texts are identical"
      accuracy = 100
    else:
      result = "Texts differ"
      # Very simple difference calculation
      common_chars = sum(1 for a, b in zip(text1, text2) if a == b)
      max_len = max(len(text1), len(text2))
      accuracy = round((common_chars / max_len) * 100, 1) if max_len > 0 else 0
    
    # Show results
    self.result_label.text = f"{result} - Similarity: {accuracy}%"
    Notification("Comparison complete", timeout=3).show()
    
    # Scroll to see results
    self.result_label.scroll_into_view()

  def open_server_test(self, **event_args):
    """Open the server test form"""
    open_form('ServerTest') 
    
  def account_link_click(self, **event_args):
    """Open the account management form"""
    open_form('AccountManagement') 