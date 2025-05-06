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

  def load_video(self, video_id):
    # This would be used to load a specific video by ID
    # For now, just show a notification
    Notification(f"Loading video with ID: {video_id}", timeout=3).show()

  def compare_button_click(self, **event_args):
    user_text = self.user_input_box.text
    official_text = self.official_input_box.text
    selected_lang = self.language_dropdown.selected_value or 'en'

    if not user_text or not official_text:
      alert("Please fill in both fields.")
      return

    # Passa o idioma selecionado, se necessário no futuro
    result = anvil.server.call("compare_transcriptions", user_text, official_text)

    self.comparison_output.content = result["html"]
    self.accuracy_label.text = (
      f"Accuracy: {result['stats']['accuracy']}% — "
      f"{result['stats']['correct']} correct, "
      f"{result['stats']['incorrect']} wrong, "
      f"{result['stats']['missing']} missing"
    )

  def search_button_click(self, **event_args):
    try:
      query = self.search_box.text
      if not query:
        alert("Please enter a search term.")
        return

      # Add simple notification to show we're searching
      Notification("Searching for videos...", timeout=2).show()
      
      # Call the server function
      results = anvil.server.call('search_youtube_videos', query)
      
      # Clear existing results
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
          
          # Add thumbnail if available
          if 'thumbnail' in video and video['thumbnail']:
            thumbnail = Image(source=video['thumbnail'], width=320, height=180)
            card.add_component(thumbnail)
          
          # Add title
          if 'title' in video and video['title']:
            title = Label(text=video['title'], role="heading")
            title.bold = True
            card.add_component(title)
          
          # Add channel
          if 'channel' in video and video['channel']:
            channel = Label(text=f"Channel: {video['channel']}")
            card.add_component(channel)
          
          # Add a button to select this video
          select_btn = Button(text="Select this video", role="primary-color")
          
          # Define a function to handle the button click with this specific video
          def create_click_handler(vid):
            def handler(**event_args):
              Notification(f"Selected video: {vid['title']}", timeout=2).show()
              # Could load the video or set up transcription here
            return handler
          
          select_btn.set_event_handler('click', create_click_handler(video))
          card.add_component(select_btn)
          
          # Add the card to the results container
          results_container.add_component(card)
      
      # Replace the existing results with the new ones
      self.content_panel.clear()
      self.content_panel.add_component(self.language_dropdown)
      self.content_panel.add_component(self.search_box)
      self.content_panel.add_component(self.search_button)
      self.content_panel.add_component(results_container)
      self.content_panel.add_component(self.user_input_box)
      self.content_panel.add_component(self.compare_button)
      self.content_panel.add_component(self.comparison_output)
      self.content_panel.add_component(self.accuracy_label)
      self.content_panel.add_component(self.official_input_box)
      
    except Exception as e:
      # If an error occurs, display it
      alert(f"Error performing search: {str(e)}")

  def user_input_box_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass

  def language_dropdown_change(self, **event_args):
    """Called when the language is changed"""
    selected = self.language_dropdown.selected_value
    Notification(f"Language set to: {selected}", timeout=2).show()
