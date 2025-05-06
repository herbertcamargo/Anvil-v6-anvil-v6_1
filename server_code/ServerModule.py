import anvil.server
from anvil.tables import app_tables
import anvil.http

@anvil.server.callable
def hello():
  return "Hello from the Anvil server!"

@anvil.server.callable
def search_youtube(query):
  """Search YouTube for videos matching the query
  
  In a real implementation, this would use the YouTube API.
  For demonstration purposes, this returns mock data.
  
  Args:
      query: Search terms
      
  Returns:
      List of video data dictionaries with id, title, thumbnail_url
  """
  # In a real implementation, you would use the YouTube API:
  # api_key = app_tables.settings.get(name="youtube_api_key")["value"]
  # url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=12&key={api_key}"
  # response = anvil.http.request(url, json=True)
  
  # Instead, we'll return mock results for demonstration
  # In a production app, you'd use the YouTube Data API
  videos = [
    {
      'id': 'dQw4w9WgXcQ',
      'title': f'YouTube Result 1 for: {query}',
      'thumbnail_url': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
    },
    {
      'id': 'QvKBP1PbSjE',
      'title': f'YouTube Result 2 for: {query}',
      'thumbnail_url': 'https://i.ytimg.com/vi/QvKBP1PbSjE/mqdefault.jpg',
    },
    {
      'id': 'G1IbRujko-A', 
      'title': f'YouTube Result 3 for: {query}',
      'thumbnail_url': 'https://i.ytimg.com/vi/G1IbRujko-A/mqdefault.jpg',
    },
    {
      'id': '7PJA0p-kzOo',
      'title': f'YouTube Result 4 for: {query}',
      'thumbnail_url': 'https://i.ytimg.com/vi/7PJA0p-kzOo/mqdefault.jpg',
    },
    {
      'id': 'KpOtuoHL45Y',
      'title': f'YouTube Result 5 for: {query}',
      'thumbnail_url': 'https://i.ytimg.com/vi/KpOtuoHL45Y/mqdefault.jpg',
    },
    {
      'id': 'OPf0YbXqDm0',
      'title': f'YouTube Result 6 for: {query}',
      'thumbnail_url': 'https://i.ytimg.com/vi/OPf0YbXqDm0/mqdefault.jpg',
    },
    {
      'id': 'J--0d3tFTI4',
      'title': f'YouTube Result 7 for: {query}',
      'thumbnail_url': 'https://i.ytimg.com/vi/J--0d3tFTI4/mqdefault.jpg',
    },
    {
      'id': '2vjPBrBU-TM',
      'title': f'YouTube Result 8 for: {query}',
      'thumbnail_url': 'https://i.ytimg.com/vi/2vjPBrBU-TM/mqdefault.jpg',
    },
    {
      'id': '09R8_2nJtjg',
      'title': f'YouTube Result 9 for: {query}',
      'thumbnail_url': 'https://i.ytimg.com/vi/09R8_2nJtjg/mqdefault.jpg',
    }
  ]
  
  return videos 