from ._anvil_designer import CompareTranscriptionTemplate
from anvil import *
import anvil.server
import anvil.users


class CompareTranscription(CompareTranscriptionTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Initialize language dropdown
    self.language_dropdown.items = [
      ('English', 'en'),
      ('Spanish', 'es'),
      ('French', 'fr'),
      ('German', 'de'),
      ('Portuguese', 'pt')
    ]
    self.language_dropdown.selected_value = 'en'
    
    # Initialize the video_id parameter if passed
    video_id = properties.get('video_id')
    if video_id:
      # Handle the video_id if needed
      self.load_video(video_id)
      
    # Test the server connection on load
    try:
      test_result = anvil.server.call('test_server_function')
      print(f"Server connection test: {test_result['message']}")
    except Exception as e:
      print(f"Server connection test failed: {str(e)}")

  def load_video(self, video_id):
    # This would be used to load a specific video by ID
    # For now, just show a notification
    Notification(f"Loading video with ID: {video_id}", timeout=3).show()

  def search_link_click(self, **event_args):
    """Show search section"""
    # No need to navigate, just scroll to search
    self.search_box.focus()
    
  def comparison_link_click(self, **event_args):
    """Show comparison section"""
    # No need to navigate, just scroll to comparison
    self.user_input_box.focus()

  def compare_button_click(self, **event_args):
    try:
      user_text = self.user_input_box.text
      official_text = self.official_input_box.text
      selected_lang = self.language_dropdown.selected_value or 'en'

      if not user_text or not official_text:
        alert("Please fill in both fields.")
        return

      Notification("Comparing texts...", timeout=2).show()
      
      # Call the server function
      result = anvil.server.call("compare_transcriptions", user_text, official_text)

      if not result or 'html' not in result or 'stats' not in result:
        raise ValueError("Invalid comparison result from server")
        
      self.comparison_output.content = result["html"]
      self.accuracy_label.text = (
        f"Accuracy: {result['stats']['accuracy']}% — "
        f"{result['stats']['correct']} correct, "
        f"{result['stats']['incorrect']} wrong, "
        f"{result['stats']['missing']} missing"
      )
      
      Notification("Comparison complete", timeout=2).show()
    except Exception as e:
      alert(f"Error comparing texts: {str(e)}")
      # Fall back to client-side comparison if server fails
      self._client_side_comparison(user_text, official_text)

  def search_button_click(self, **event_args):
    try:
      query = self.search_box.text
      if not query:
        alert("Please enter a search term.")
        return

      # First test the server connection with a simple function
      try:
        Notification("Testing minimal server function...", timeout=2).show()
        minimal_result = anvil.server.call('minimal_test')
        Notification(f"Minimal test result: {minimal_result}", timeout=2).show()
      except Exception as e:
        # If server test fails, fall back to client-side search
        Notification("Server unavailable. Using client-side search.", timeout=3).show()
        self._client_side_search(query)
        return

      # Try the actual search
      try:
        Notification("Searching for videos...", timeout=2).show()
        results = anvil.server.call('search_youtube_videos', query)
        Notification(f"Search returned {len(results)} results", timeout=2).show()
      except Exception as e:
        # If server search fails, fall back to client-side search
        Notification("Server search failed. Using client-side search.", timeout=3).show()
        self._client_side_search(query)
        return
      
      # Create results display
      results_container = ColumnPanel()
      results_container.spacing_above = "large"
      
      if not results:
        results_container.add_component(Label(text="No results found", role="headline"))
      else:
        results_container.add_component(Label(text=f"Found {len(results)} videos", role="headline"))
        
        # Add each video as a simple card
        for video in results:
          # Create a card for each mock result
          card = ColumnPanel(spacing="medium")
          card.border = "1px solid #ddd"
          # Set spacing to emulate padding
          card.spacing = ("medium", "medium", "medium", "medium")
          card.spacing_below = "medium"
          
          # Create a placeholder image that won't cause errors
          thumbnail = Image(source=None, width=320, height=180)
          thumbnail.background = "#f0f0f0"  # Gray background for placeholder
          card.add_component(thumbnail)
          
          # Add title (use a default if missing)
          title_text = video.get('title', 'Unknown Title')
          title = Label(text=title_text, role="heading")
          title.bold = True
          card.add_component(title)
          
          # Add channel (use a default if missing)
          channel_text = f"Channel: {video.get('channel', 'Unknown Channel')}"
          channel = Label(text=channel_text)
          card.add_component(channel)
          
          # Add a button to select this video
          select_btn = Button(text="Select Video", role="primary")
          card.add_component(select_btn)
          
          # Add the card to the results container
          results_container.add_component(card)
          
      # Update the repeater with the results
      self.results_repeater.items = results
      
    except Exception as e:
      # If an error occurs, display it
      alert(f"Error processing search results: {str(e)}")
      # Fall back to client-side search
      self._client_side_search(query)
      
  def _client_side_search(self, query):
    """Fallback client-side search when server is unavailable"""
    # Create mock results without calling the server
    results = []
    self.results_repeater.items = results
    
    # Create a results panel
    results_panel = ColumnPanel()
    
    # Add a heading
    results_panel.add_component(Label(text=f"Results for: {query} (Client-side mock)", role="heading"))
    
    # Add some mock results
    for i in range(3):
      # Create a card for each mock result
      card = ColumnPanel()
      card.spacing_above = "medium"
      card.spacing_below = "medium"
      card.border = "1px solid #ddd"
      
      # Add mock title and info
      title = Label(text=f"Mock result {i+1} for {query}", role="heading")
      title.bold = True
      info = Label(text="This is a client-side only mock result (no server call)")
      
      card.add_component(title)
      card.add_component(info)
      
      results_panel.add_component(card)
    
    # Replace results_repeater with this panel
    parent = self.results_repeater.parent
    index = parent.get_components().index(self.results_repeater)
    parent.remove_component(self.results_repeater)
    parent.add_component(results_panel, index=index)
    
    # Show a notification
    Notification("Found 3 mock results (client-side only)", timeout=3).show()
    
  def _client_side_comparison(self, text1, text2):
    """Fallback client-side comparison when server is unavailable"""
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
    self.comparison_output.content = f"<span style='color:blue'>CLIENT-SIDE COMPARISON:</span><br>{result}"
    self.accuracy_label.text = f"Similarity: {accuracy}% (client-side calculation)"
    Notification("Completed client-side comparison", timeout=3).show()

  def user_input_box_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass

  def language_dropdown_change(self, **event_args):
    """Called when the language is changed"""
    selected = self.language_dropdown.selected_value
    Notification(f"Language set to: {selected}", timeout=2).show()
