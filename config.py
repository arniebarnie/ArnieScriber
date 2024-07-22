import json
import os
from os import path

CONFIG = None

def GlobalConfig():
    """
    Reads in the configuration from the config.json file
    """
    global CONFIG

    if CONFIG is None:
        with open('config.json') as file:
            CONFIG = json.load(file)
    
        for directory in ['temp', 'results']:
            CONFIG[directory] = path.abspath(CONFIG[directory])

            if not os.path.isdir(CONFIG[directory]):
                os.mkdir(CONFIG[directory])

    return CONFIG