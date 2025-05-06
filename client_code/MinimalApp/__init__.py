from ._anvil_designer import MinimalAppTemplate
from anvil import *
import anvil.js

class MinimalApp(MinimalAppTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Set all panels visible
    self.show_all_panels()
    
    # Initialize video functionality
    self.setup_youtube_functionality()
    
    # Add debug button
    self.debug_button = Button(text="Debug HTML", role="secondary")
    self.debug_button.set_event_handler('click', self.debug_html)
    self.search_panel.add_component(self.debug_button, index=1)
    
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
    self.grid_html = Html(parent=self.yt_grid_container)
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
    self.player_html = Html(parent=self.yt_player_container)
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
    
    # Try a simpler approach - create all thumbnails using a single innerHTML update
    html_content = ""
    
    for i, video in enumerate(videos_data[:12]):
      video_id = video.get('id', '')
      title = video.get('title', 'Untitled video')
      thumbnail_url = video.get('thumbnail_url', 'https://via.placeholder.com/320x180')
      
      # Create the HTML for this thumbnail
      html_content += f"""
      <div class="thumbnail-container" data-video-id="{video_id}" data-index="{i}" onclick="anvil.call('thumbnail_click', {i})">
        <img src="{thumbnail_url}" alt="{title}" class="thumbnail-image">
        <p class="video-title">{title}</p>
      </div>
      """
    
    # Set the HTML content
    grid_container.innerHTML = html_content
      
  def thumbnail_click(self, index):
    """Handle thumbnail click from HTML"""
    if index < len(self.videos):
      self.play_video(self.videos[index])
    
  def play_video(self, video_data):
    """Play the specified video"""
    video_id = video_data.get('id')
    if not video_id:
      return
      
    # Update the iframe src with the new video ID
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
    if title_element and video_data.get('title'):
      title_element.textContent = video_data.get('title')
      
    # Scroll to player
    self.yt_player_container.scroll_into_view()
    
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
      }
    ]
    
    # Create a separate notification showing we're updating thumbnails
    Notification("Preparing to update thumbnails...", timeout=2).show()
    
    try:
      # Update the YouTube grid with new videos
      self.update_youtube_grid(videos)
      
      # Show a notification of success
      Notification(f"Successfully added {len(videos)} videos to grid", timeout=3).show()
    except Exception as e:
      # Show error notification if update fails
      alert(f"Error updating grid: {str(e)}")
    
    # Also show text search results for consistency
    self.results_panel.clear()
    self.results_panel.add_component(Label(text=f"Text Results for: {query}", role="heading"))
    
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
      
    # Scroll to both results
    self.yt_grid_container.scroll_into_view()
    
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