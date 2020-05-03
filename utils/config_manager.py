from cryptography.fernet import Fernet
from json import loads

config_key = open('./security/key.key', 'rb').read()
f = Fernet(config_key)
config = loads(f.decrypt(open('config.json', 'rb').read()))

def get_secret_key():
    return config['secret_key'].split("'")[1].encode('utf-8')

def get(key):
    return config[key]
