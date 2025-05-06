from ._anvil_designer import ServerTestTemplate
from anvil import *
import anvil.server

class ServerTest(ServerTestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def test_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      self.result_label.text = "Testing server connection..."
      result = anvil.server.call('minimal_test')
      self.result_label.text = f"Server test result: {result}"
      self.result_label.foreground = "#00aa00"  # Green for success
    except Exception as e:
      self.result_label.text = f"Error: {str(e)}"
      self.result_label.foreground = "#aa0000"  # Red for error 