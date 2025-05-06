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

  def search_button_click(self, **event_args):
    try:
      query = self.search_box.text
      if not query:
        alert("Please enter a search term.")
        return

      # Try a completely minimal test first
      try:
        Notification("Testing minimal server function...", timeout=2).show()
        minimal_result = anvil.server.call('minimal_test')
        Notification(f"Minimal test result: {minimal_result}", timeout=2).show()
      except Exception as e:
        alert(f"Minimal server test failed: {str(e)}")
        return

      # First test the server connection with a simple function
      try:
        Notification("Testing server connection...", timeout=2).show()
        test_result = anvil.server.call('test_server_function')
        Notification(f"Server test: {test_result['message']}", timeout=2).show()
      except Exception as e:
        alert(f"Server connection test failed: {str(e)}")
        return

      # If server test passed, try the search
      try:
        Notification("Searching for videos...", timeout=2).show()
        results = anvil.server.call('search_youtube_videos', query)
        Notification(f"Search returned {len(results)} results", timeout=2).show()
      except Exception as e:
        alert(f"Server search error: {str(e)}")
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
          # Create a card for each video
          card = ColumnPanel(spacing="medium")
          card.border = "1px solid #ddd"
          card.padding = 10
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
      
      # Replace the existing results with the new ones
      self.content_panel.clear()
      
      # Create a search controls panel
      search_controls = FlowPanel()
      search_controls.add_component(self.language_dropdown)
      search_controls.add_component(self.search_box)
      search_controls.add_component(self.search_button)
      
      self.content_panel.add_component(search_controls)
      self.content_panel.add_component(results_container)
      
      # Add the transcription components
      transcription_panel = ColumnPanel()
      transcription_panel.add_component(self.user_input_box)
      transcription_panel.add_component(self.compare_button)
      transcription_panel.add_component(self.comparison_output)
      transcription_panel.add_component(self.accuracy_label)
      transcription_panel.add_component(self.official_input_box)
      
      self.content_panel.add_component(transcription_panel)
      
    except Exception as e:
      # If an error occurs, display it
      alert(f"Error processing search results: {str(e)}")

  def user_input_box_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass

  def language_dropdown_change(self, **event_args):
    """Called when the language is changed"""
    selected = self.language_dropdown.selected_value
    Notification(f"Language set to: {selected}", timeout=2).show()
