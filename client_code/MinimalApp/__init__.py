from ._anvil_designer import MinimalAppTemplate
from anvil import *

class MinimalApp(MinimalAppTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Set default view - show welcome panel only
    self.show_welcome_panel()
    
  def show_welcome_panel(self):
    """Show only the welcome panel"""
    self.welcome_panel.visible = True
    self.search_panel.visible = False
    self.compare_panel.visible = False
    
  def show_all_panels(self):
    """Show all main panels (but not welcome)"""
    self.welcome_panel.visible = False
    self.search_panel.visible = True
    self.compare_panel.visible = True
    
  def show_search_panel_only(self):
    """Show only the search panel"""
    self.welcome_panel.visible = False
    self.search_panel.visible = True
    self.compare_panel.visible = False
    
  def show_compare_panel_only(self):
    """Show only the comparison panel"""
    self.welcome_panel.visible = False
    self.search_panel.visible = False
    self.compare_panel.visible = True
    
  def home_link_click(self, **event_args):
    """Handle click on Home link"""
    self.show_welcome_panel()
    
  def search_link_click(self, **event_args):
    """Handle click on Search link"""
    self.show_search_panel_only()
    
  def comparison_link_click(self, **event_args):
    """Handle click on Comparison link"""
    self.show_compare_panel_only()
    
  def welcome_search_button_click(self, **event_args):
    """Handle click on Start Searching button"""
    self.show_search_panel_only()
    
  def welcome_compare_button_click(self, **event_args):
    """Handle click on Practice Comparison button"""
    self.show_compare_panel_only()
  
  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Use client-side only functionality - no server calls
    query = self.search_box.text
    if not query:
      alert("Please enter a search term")
      return
      
    # Create mock results without calling the server
    self.results_panel.clear()
    
    # Add a heading
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
      
    # Show a notification
    Notification("Found 3 mock results", timeout=3).show()
    
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

  def open_server_test(self, **event_args):
    """Open the server test form"""
    open_form('ServerTest') 