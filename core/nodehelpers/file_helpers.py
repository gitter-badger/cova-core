import os

def get_absolute_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)