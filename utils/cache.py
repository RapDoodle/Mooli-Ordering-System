db = {}

def get(key):
    if key in db:
        return db[key]
    return None

def set(key, value):
    db[key] = value