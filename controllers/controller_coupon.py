import models.model_coupon as m
from utils.exception import excpetion_handler

@excpetion_handler
def add_coupon(*args, **kwargs):
    return m.add_coupon(*args, **kwargs)

@excpetion_handler
def update_coupon(*args, **kwargs):
    return m.update_coupon(*args, **kwargs)

@excpetion_handler
def delete_coupon(*args, **kwargs):
    return m.delete_coupon(*args, **kwargs)

@excpetion_handler
def get_coupons():
    return m.get_coupons()

@excpetion_handler
def find_coupon(*args, **kwargs):
    return m.find_coupon(*args, **kwargs)

@excpetion_handler
def check_coupon_validity(coupon_code, user_id):
    # Check if the coupon is valid
    coupon = m.find_coupon_and_check_validity(coupon_code)
    # No errors raised, check if the user is eligible for the coupon
    from controllers.controller_cart_item import get_user_cart_total
    if coupon is not None:
        if get_user_cart_total(user_id) < coupon['threshold']:
            return False
        return True
    else:
        return False