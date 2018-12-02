import os

def load_config(config_filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), config_filename)