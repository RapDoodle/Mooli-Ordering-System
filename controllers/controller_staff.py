import models.model_staff as m
from utils.exception import excpetion_handler

@excpetion_handler
def add_staff(*args, **kwargs):
    return m.add_staff(*args, **kwargs)

@excpetion_handler
def find_staff(*args, **kwargs):
    return m.find_staff(*args, **kwargs)

@excpetion_handler
def get_staff_list(*args, **kwargs):
    return m.get_staff_list(*args, **kwargs)

@excpetion_handler
def update_staff(*args, **kwargs):
    return m.update_staff(*args, **kwargs)

@excpetion_handler
def delete_staff(*args, **kwargs):
    return m.delete_staff(*args, **kwargs)