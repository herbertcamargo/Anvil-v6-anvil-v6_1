from ._anvil_designer import ServerTestTemplate
from anvil import *
import anvil.server

class ServerTest(ServerTestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Show diagnostic information
    try:
      app_info = """
      Application: Anvil-v6
      Environment: Client-side
      Status: Form loaded
      """
      self.info_label.text = app_info
    except:
      pass

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
      self.result_label.text = "Returning to main app..."
      open_form('CompareTranscription')
    except Exception as e:
      self.result_label.text = f"Error returning to main app: {str(e)}"
      self.result_label.foreground = "#aa0000"  # Red for error 