import models.model_order as m
from utils.exception import excpetion_handler

@excpetion_handler
def place_order(user_id, coupon_code = ''):
    return m.place_order(
        user_id = user_id, 
        payment = 'balance', 
        coupon_code = coupon_code
    )

@excpetion_handler
def get_on_going_orders():
    return m.get_orders(scope = 'on_going')

@excpetion_handler
def get_order_purchased_items(order_id):
    return m.get_order_purchased_items(order_id)
    
@excpetion_handler
def update_order_status(*args, **kwargs):
    return m.update_order_status(*args, **kwargs)

@excpetion_handler
def get_order(*args, **kwargs):
    return m.get_order(*args, **kwargs)

@excpetion_handler
def get_all_orders(page):
    # Each page contains 20 records
    try:
        page = int(page)
    except:
        page = 1
    return m.get_orders(scope = 'all', limit = 20, offset = (page - 1) * 20)

@excpetion_handler
def order_refund(*args, **kwargs):
    return m.order_refund(*args, **kwargs)

@excpetion_handler
def count_records_length():
    return m.count_records_length()