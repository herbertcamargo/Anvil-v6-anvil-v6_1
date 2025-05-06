import anvil.server
from anvil.tables import app_tables
import anvil.users
import anvil.tables.query as q
import re
import difflib

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
  """Mock function to search YouTube videos"""
  # In a real app, this would call the YouTube API
  # For now, return mock data
  if not query:
    return []
  
  # Mock video results
  videos = [
    {
      'id': 'video1',
      'title': f'Sample video about {query}',
      'thumbnail': 'https://via.placeholder.com/320x180',
      'channel': 'Sample Channel'
    },
    {
      'id': 'video2',
      'title': f'Learn about {query} - Tutorial',
      'thumbnail': 'https://via.placeholder.com/320x180',
      'channel': 'Education Channel'
    },
    {
      'id': 'video3',
      'title': f'{query} for beginners',
      'thumbnail': 'https://via.placeholder.com/320x180',
      'channel': 'Tutorial Channel'
    }
  ]
  
  return videos

@anvil.server.callable
def compare_transcriptions(user_text, official_text):
  """Compare a user's transcription with the official one"""
  # Clean up the texts
  user_words = re.findall(r'\b\w+\b', user_text.lower())
  official_words = re.findall(r'\b\w+\b', official_text.lower())
  
  # Use difflib to do the comparison
  matcher = difflib.SequenceMatcher(None, user_words, official_words)
  
  # Generate HTML diff
  diff_html = ""
  total_words = len(official_words)
  correct_words = 0
  incorrect_words = 0
  missing_words = 0
  
  for tag, i1, i2, j1, j2 in matcher.get_opcodes():
    if tag == 'equal':
      # Words match
      diff_html += '<span style="color: green; font-weight: bold;">' + ' '.join(user_words[i1:i2]) + '</span> '
      correct_words += (i2 - i1)
    elif tag == 'replace':
      # Words don't match
      diff_html += '<span style="color: red; text-decoration: line-through;">' + ' '.join(user_words[i1:i2]) + '</span> '
      diff_html += '<span style="color: blue;">[' + ' '.join(official_words[j1:j2]) + ']</span> '
      incorrect_words += (i2 - i1)
    elif tag == 'delete':
      # Extra words in user text
      diff_html += '<span style="color: orange; text-decoration: line-through;">' + ' '.join(user_words[i1:i2]) + '</span> '
      incorrect_words += (i2 - i1)
    elif tag == 'insert':
      # Missing words in user text
      diff_html += '<span style="color: purple;">[' + ' '.join(official_words[j1:j2]) + ']</span> '
      missing_words += (j2 - j1)
  
  # Calculate accuracy
  accuracy = 0
  if total_words > 0:
    accuracy = round((correct_words / total_words) * 100, 1)
  
  return {
    'html': diff_html,
    'stats': {
      'accuracy': accuracy,
      'correct': correct_words,
      'incorrect': incorrect_words,
      'missing': missing_words
    }
  } 