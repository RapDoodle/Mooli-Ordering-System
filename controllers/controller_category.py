import models.model_category as model_category
from utils.exception import excpetion_handler

@excpetion_handler
def add_category(name, priority):
    model_category.add_category(name, priority)

@excpetion_handler
def update_category(category_id, category_name, priority):
    model_category.update_category(category_id, category_name, priority)

@excpetion_handler
def remove_category(id):
    model_category.remove_category(id)

@excpetion_handler
def list_categories():
    return_dict = model_category.get_category_list()
    if len(return_dict) == 0:
        return []
    return return_dict
