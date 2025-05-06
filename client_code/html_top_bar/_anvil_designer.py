from anvil import *

# Define template classes for our custom components
class YouTubeGridTemplate(Container):
  def __init__(self, **properties):
    properties.setdefault('container', ColumnPanel())
    super().__init__(**properties)
    self.grid_html = Html(parent=self)

class YouTubePlayerTemplate(Container):
  def __init__(self, **properties):
    properties.setdefault('container', ColumnPanel())
    super().__init__(**properties)
    self.player_html = Html(parent=self) 