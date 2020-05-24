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
    orders = m.get_orders(scope = 'on_going')
    for order in orders:
        total = 0
        order_items = m.get_order_purchased_items(order['order_id'])
        for order_item in order_items:
            total += order_item['product_price_snapshot'] * order_item['amount']
        order['total'] = total
    return orders

@excpetion_handler
def get_order_purchased_items(order_id):
    return m.get_order_purchased_items(order_id)
    
@excpetion_handler
def update_order_status(*args, **kwargs):
    return m.update_order_status(*args, **kwargs)

@excpetion_handler
def get_all_orders():
    orders = m.get_orders(scope = 'all')
    for order in orders:
        total = 0
        order_items = m.get_order_purchased_items(order['order_id'])
        for order_item in order_items:
            total += order_item['product_price_snapshot'] * order_item['amount']
        order['total'] = total
    return orders