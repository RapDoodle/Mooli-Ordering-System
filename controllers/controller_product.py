import models.model_product as m
from utils.exception import excpetion_handler

@excpetion_handler
def add_product(*args, **kwargs):
    m.add_product(*args, **kwargs)

@excpetion_handler
def edit_product(*args, **kwargs):
    m.update_product(*args, **kwargs)

@excpetion_handler
def remove_product(product_id):
    m.remove_product(product_id)

@excpetion_handler
def get_products_by_id(product_id):
    return_dict = m.find_product('product_id', product_id)
    if len(return_dict) == 0:
        return []
    return return_dict

@excpetion_handler
def get_products_by_category_id(category_id):
    return_dict = m.get_products('category_id', category_id)
    if len(return_dict) == 0:
        return []
    return return_dict

@excpetion_handler
def get_all_products():
    return m.get_products('all')

@excpetion_handler
def get_product_by_name(product_name):
    return_dict = m.find_product('product_name', product_name)
    return return_dict

@excpetion_handler
def get_product_by_product_id(product_id):
    return m.find_product('product_id', product_id)
