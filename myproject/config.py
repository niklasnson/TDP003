import json

def load(filename): 
    with open(filename) as config_file:
       config = json.load(config_file) 
    return config

