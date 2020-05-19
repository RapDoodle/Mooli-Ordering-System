"""The module deals with all the IOs with the file system """

from utils.exception import ValidationError
import os

THUMBNAIL_PATH = './static/media/thumbnails'
PICTURE_PATH = './static/media/pictures'

# Initialize the paths if not exist
if not os.path.exists(THUMBNAIL_PATH):
    os.mkdir(THUMBNAIL_PATH)
if not os.path.exists(PICTURE_PATH):
    os.mkdir(PICTURE_PATH)

def save_thumbnail(product_id, f):
    save(os.path.join(THUMBNAIL_PATH, str(product_id)), f)

def save_picture(product_id, f):
    save(os.path.join(PICTURE_PATH, str(product_id)), f)

def save(path, f):
    f.save(path)

def get_thumbnail_path(product_id):
    get_path(THUMBNAIL_PATH, product_id)

def get_picture_path(product_id):
    get_path(PICTURE_PATH, product_id)

def get_path(prefix, product_id):
    return os.path.join()