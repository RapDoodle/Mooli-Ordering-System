import models.model_comment as m
from utils.exception import excpetion_handler

@excpetion_handler
def add_comment(*args, **kwargs):
    return m.add_comment(*args, **kwargs)

@excpetion_handler
def get_product_ratings(*args, **kwargs):
    return m.get_product_ratings(*args, **kwargs)