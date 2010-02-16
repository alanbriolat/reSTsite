import yaml

settings = dict()

def load_settings(filepath):
    """
    Load settings from a YAML file
    """
    global settings
    settings.clear()
    settings.update(yaml.load(open(filepath, 'r').read()))
