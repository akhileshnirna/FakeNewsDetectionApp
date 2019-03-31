import os
import sys

def get_path(ss):
  return os.path.join(os.path.dirname(__file__), ss)

sys.path += [
  get_path('api'), 
  get_path('ml')
]