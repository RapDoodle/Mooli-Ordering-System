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