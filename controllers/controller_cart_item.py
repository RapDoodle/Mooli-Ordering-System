import models.model_cart_item as model_cart_item
from utils.exception import excpetion_handler

@excpetion_handler
def create_cart_item(*args, **kwargs):
    return model_cart_item.create_cart_item(*args, **kwargs)

@excpetion_handler
def update_cart_item_amount(*args, **kwargs):
    return model_cart_item.update_cart_item_amount(*args, **kwargs)

@excpetion_handler
def delete_cart_item(*args, **kwargs):
    return model_cart_item.delete_cart_item(*args, **kwargs)

@excpetion_handler
def get_cart_items_by_user_id(*args, **kwargs):
    return model_cart_item.get_cart_items_by_user_id(*args, **kwargs)
