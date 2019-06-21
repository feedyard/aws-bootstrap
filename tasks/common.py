import json

def load_config(config_file):
    """Load *.json config file"""
    if config_file.is_file():
        return json.loads(open(config_file).read())
    print('missing {} file.'.format(config_file))
    sys.exit(1)
