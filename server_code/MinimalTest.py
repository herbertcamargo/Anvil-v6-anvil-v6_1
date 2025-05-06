import anvil.server

@anvil.server.callable
def minimal_test():
  """Absolute minimal function to test server environment"""
  return "ok" 