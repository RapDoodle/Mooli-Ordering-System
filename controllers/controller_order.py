import models.model_order as m
from utils.exception import excpetion_handler

@excpetion_handler
def place_order(user_id, coupon_code = ''):
    return m.place_order(
        user_id = user_id, 
        payment = 'balance', 
        coupon_code = coupon_code
    )