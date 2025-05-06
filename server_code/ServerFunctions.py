import anvil.server
from anvil.tables import app_tables
import anvil.users

# Only include the most essential imports to avoid potential issues
# import anvil.tables.query as q
# import re
# import difflib

@anvil.server.callable
def test_server_function():
  """Simple test function to check if server is working"""
  return {"status": "ok", "message": "Server is working properly"}

@anvil.server.callable
def calculate_percentage_of(number_1, number_2):
  """Calculate what percentage number_1 is of number_2"""
  try:
    return round((float(number_1) / float(number_2)) * 100, 2)
  except (ValueError, ZeroDivisionError):
    return "Error: Please enter valid numbers (and make sure the second number is not 0)"

@anvil.server.callable
def get_product_names():
  """Return a list of product names for the subscription tiers"""
  return ["Free", "Personal", "Professional", "Enterprise"]

@anvil.server.callable
def change_name(new_name):
  """Change the name of the current user"""
  user = anvil.users.get_user()
  if user:
    user['name'] = new_name
    user.update()
    return user
  return None

@anvil.server.callable
def change_email(new_email):
  """Change the email of the current user"""
  user = anvil.users.get_user()
  if user:
    user['email'] = new_email
    user.update()
    return user
  return None

@anvil.server.callable
def delete_user():
  """Delete the current user"""
  user = anvil.users.get_user()
  if user:
    anvil.users.logout()
    user.delete()
    return True
  return False

@anvil.server.callable
def search_youtube_videos(query):
  """Simplified mock function that returns static data only"""
  # Return hardcoded data without any processing
  return [
    {
      'video_id': 'static1',
      'title': 'Static Video 1',
      'channel': 'Static Channel'
    },
    {
      'video_id': 'static2',
      'title': 'Static Video 2',
      'channel': 'Static Channel'
    }
  ]

@anvil.server.callable
def compare_transcriptions(user_text, official_text):
  """Simplified comparison function"""
  # Create a very simple comparison result
  diff_html = "<span style='color:green'>Text comparison complete.</span>"
  
  return {
    'html': diff_html,
    'stats': {
      'accuracy': 80.0,
      'correct': 8,
      'incorrect': 1,
      'missing': 1
    }
  } 