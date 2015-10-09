import json

def load(filename): 
    try:
        with open(filename) as config_file:
            config = json.load(config_file) 
        return config
    except: 
        return None
