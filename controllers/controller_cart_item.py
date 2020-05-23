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

@excpetion_handler
def get_user_cart_total(user_id):
    cart_items = model_cart_item.get_cart_items_by_user_id(user_id)
    total = 0
    if cart_items is not None:
        for cart_item in cart_items:
            total += cart_item['price'] * cart_item['amount']
    return total