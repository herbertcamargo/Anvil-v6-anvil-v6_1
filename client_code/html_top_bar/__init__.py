from ._anvil_designer import html_top_barTemplate
from anvil import *
import anvil.server
import anvil.users


class html_top_bar(html_top_barTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
