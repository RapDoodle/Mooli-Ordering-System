from utils.validation import is_money
from models.DAO import DAO
from utils.exception import ValidationError
from models.shared import (
    user_pay, 
    find_user, 
    find_coupon_and_check_validity, 
    create_purchased_item,
    get_cart_items_by_user_id,
    delete_cart_item
)

def place_order(user_id, payment, coupon_code = ''):
    """The function places an order of all the items in the user's cart

    Parameters:
    user_id -- the user's id
    payment -- the method the user chose to pay
    coupon_code -- the coupon code (if any)
    """
    # Check the validity of the payment method
    if payment not in ['balance', 'credit_card', 'paypal']:
        raise ValidationError('Invalid payment method.')

    # Clean the input data
    user_id = str(user_id).strip()
    if coupon_code is None:
        coupon_code = ''
    coupon_code = str(coupon_code).strip()

    # Retrive coupon data
    coupon = find_coupon_and_check_validity(coupon_code)

    # If the user did input a coupon but the coupon is invalid
    if len(coupon_code) > 0 and coupon is None:
        raise ValidationError('Invalid coupon code.')

    # Check for the existence of user
    if find_user(method = 'id', param = user_id) is None:
        raise ValidationError('Invalid user id.')

    # Check the user's cart. If the item already exists, perform update instead of amount
    items = get_cart_items_by_user_id(user_id)
    if len(items) == 0:
        raise ValidationError('No item is found in cart.')

    # Calculate the total in the user's cart
    total = 0
    for item in items:
        total += item['price'] * item['amount']
    actual_paid = total

    # Calculate according to the given coupon
    if coupon is not None:
        if total >= coupon['threshold']:
            actual_paid -= coupon['value']

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Proceed to the payment
    if payment == 'balance':
        user_pay(user_id, actual_paid, cursor)
    else:
        raise ValidationError('The payment method is not supported by the current merchant.')

    # Create new order
    sql = """INSERT INTO `order` (
        actual_paid
    ) VALUES (
        %(actual_paid)s
    )"""
    cursor.execute(sql, {'actual_paid': actual_paid})

    # Retrive the newly inserted row
    cursor.execute('SELECT LAST_INSERT_ID()')
    order_id = cursor.fetchone()['LAST_INSERT_ID()']

    # Insert into user_order
    sql = """INSERT INTO user_order (
        user_id,
        order_id
    ) VALUES (
        %(user_id)s,
        %(order_id)s
    )"""
    cursor.execute(sql, {'user_id':user_id,
                        'order_id': order_id})

    for item in items:
        create_purchased_item(
            product_name = item['product_name'],
            product_price = item['price'],
            amount = item['amount'],
            order_id = order_id,
            cursor = cursor
        )
        delete_cart_item(
            cart_item_id = item['cart_item_id'],
            relay_cursor = cursor
        )
    
    # When all the procedures are successful and no exception was raised
    dao.commit()

def place_redeem(user_id, amount):
    # Clean the input data
    user_id = str(user_id).strip()
    amount = str(amount).strip()

    # Verify the amount
    if not is_money(amount):
        raise ValidationError('Invalid amount.')

    # Verify the user_id
    if find_user(method = 'id', param = user_id) is None:
        raise ValidationError('Invalid user id.')

    # Insert into order
    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """INSERT INTO `order` (
        user_id,
        total,
        actual_paid,
        status
    ) VALUES (
        %(user_id)s,
        %(total)s,
        %(actual_paid)s,
        %(status)s
    )"""
    # A status code of 100 means it is a desposite
    cursor.execute(sql, {'user_id':user_id,
                        'total': -amount,
                        'actual_paid': 0,
                        'status': 100})
    dao.commit()


def update_order_status(order_id, status):
    # Clean the input data
    order_id = str(order_id).strip()
    status = str(status).strip()

    if status not in ['CANC', 'PEND', 'PROC', 'REDY', 'DONE', 'REDD']:
        raise ValidationError('Invalid status code.')

    # Check for the existence of order
    order = find_order_by_id(order_id)
    if order is None:
        raise ValidationError('Order not found.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """UPDATE `order` SET
            status = %(status)s
            WHERE order_id = %(order_id)s"""
    cursor.execute(sql, {'status': status,
                        'order_id': order_id})
    dao.commit()

def delete_order(order_id):
    # Clean the input data
    order_id = str(order_id).strip()

    # Check for existence
    if find_order_by_id(order_id) is None:
        raise ValidationError('Order not found.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """DELETE FROM `order` WHERE order_id = %(order_id)s"""
    cursor.execute(sql, {'order_id': order_id})

    dao.commit()

def get_user_transaction_history(user_id):
    # Clean the input data
    user_id = str(user_id).strip()

    # Check for the existence of user
    if find_user(method = 'id', param = user_id) is None:
        raise ValidationError('Invalid user id.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM `order` WHERE user_id = %(user_id)s ORDER BY created_at DESC"""
    cursor.execute(sql, {'user_id': user_id})
    result = cursor.fetchall()
    return result

def get_order_purchased_items(order_id):
    # Clean the input data
    order_id = str(order_id).strip()

    # Check for the existence of order
    order = find_order_by_id(order_id)
    if order is None:
        raise ValidationError('Order not found.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM purchased_item, archive WHERE 
                purchased_item.order_id = %(order_id)s AND
                purchased_item.product_name_snapshot = archive.archive_index
                ORDER BY archive.value ASC"""
    cursor.execute(sql, {'order_id': order_id})
    result = cursor.fetchall()
    return result

def find_order_by_id(order_id):
    # Clean the input data
    order_id = str(order_id).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM `order` WHERE
                order_id = %(order_id)s"""
    cursor.execute(sql, {'order_id': order_id})
    result = cursor.fetchone()
    return result

def get_orders(scope):
    # Verify is the scope valid
    if scope not in ['all', 'on_going']:
        raise ValidationError('Invalid scope.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    if scope == 'on_going':
        sql = """WITH s_order AS (
                    SELECT * FROM `order` WHERE status >= 2 AND 
                        status <= 4
                ) SELECT user.user_id, 
                    user.username,
                    user.first_name,
                    user.last_name,
                    s_order.order_id,
                    s_order.actual_paid,
                    s_order.status,
                    s_order.created_at
                FROM s_order, user_order, user WHERE
                    s_order.order_id = user_order.order_id AND
                    user_order.user_id = user.user_id
                ORDER BY s_order.created_at ASC"""
    elif scope == 'all':
        sql = """SELECT user.user_id, 
                    user.username,
                    user.first_name,
                    user.last_name,
                    `order`.order_id,
                    `order`.actual_paid,
                    `order`.status,
                    `order`.created_at
                FROM `order`, user_order, user WHERE
                    `order`.order_id = user_order.order_id AND
                    user_order.user_id = user.user_id
                ORDER BY `order`.created_at ASC"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result