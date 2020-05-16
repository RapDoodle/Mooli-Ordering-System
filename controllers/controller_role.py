import models.model_role as m
from utils.exception import excpetion_handler

@excpetion_handler
def add_role(*args, **kwargs):
    return m.add_role(*args, **kwargs)

@excpetion_handler
def find_role(*args, **kwargs):
    return m.find_role(*args, **kwargs)

@excpetion_handler
def get_all_roles(*args, **kwargs):
    return m.get_all_roles(*args, **kwargs)

@excpetion_handler
def update_role(*args, **kwargs):
    return m.update_role(*args, **kwargs)

@excpetion_handler
def set_role_permissions(*args, **kwargs):
    return m.set_role_permissions(*args, **kwargs)

@excpetion_handler
def add_permission(*args, **kwargs):
    return m.add_permission(*args, **kwargs)

@excpetion_handler
def find_permission(*args, **kwargs):
    return m.find_permission(*args, **kwargs)

@excpetion_handler
def get_permissions(*args, **kwargs):
    return m.get_permissions(*args, **kwargs)

@excpetion_handler
def get_all_permissions(*args, **kwargs):
    return m.get_all_permissions(*args, **kwargs)

@excpetion_handler
def delete_permission(*args, **kwargs):
    return m.delete_permission(*args, **kwargs)
