from cryptography.fernet import Fernet
from json import loads

SECURITY_KEY_PATH = './security/key.key'
SECURITY_CONFIG_PATH = './security/config.obj'
CONFIG_PATH = './config.json'

config_key = open(SECURITY_KEY_PATH, 'rb').read()
f = Fernet(config_key)
security_config = loads(f.decrypt(open(SECURITY_CONFIG_PATH, 'rb').read()))
config = loads(open(CONFIG_PATH, 'r').read())

def get_secret_key():
    return security_config['SECRET_KEY'].split("'")[1].encode('utf-8')

def get_security(key):
    try:
        return security_config[key]
    except:
        print('Warning: an attemp to read key "{}" from security config failed.'.format(key))
        return None

def set_security_temp(key, value):
    # Temporarily chaging the config of the system for testing purposes
    # DO NOT ENABLE IT IN PRODUCTION MODE
    security_config[key] = value

def get(key):
    try:
        return config[key]
    except:
        print('Warning: an attemp to read key "{}" from config failed.'.format(key))
        return None
