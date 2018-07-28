
from configparser import SafeConfigParser, NoOptionError

def load_conf(filepath):
    config = SafeConfigParser()
    config.read(filepath)
    data = {}
    for section in config.sections():
        data[section] = dict(config.items(section))
    return data

