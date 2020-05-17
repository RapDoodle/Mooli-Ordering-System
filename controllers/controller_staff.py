import models.model_staff as m
from utils.exception import excpetion_handler

@excpetion_handler
def add_staff(*args, **kwargs):
    m.add_staff(*args, **kwargs)

@excpetion_handler
def find_staff(*args, **kwargs):
    m.find_staff(*args, **kwargs)
