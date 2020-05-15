from utils.validation import is_money
from models.DAO import DAO
from utils.exception import ValidationError
from models.shared import get_items_by_user_id, find_user, find_coupon_and_check_validity, get_items_by_user_id, get_archive_index

def place_order(user_id, coupon_code = ''):
    # Clean the input data
    user_id = str(user_id).strip()
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
    items = get_items_by_user_id(user_id = user_id, scope = 'cart')
    if len(items) == 0:
        raise ValidationError('No item found in cart.')

    # Calculate the total in the user's cart
    total = 0
    for item in items:
        total += item['price'] * item['amount']
    actual_paid = total

    # Calculate according to the given coupon
    if total >= coupon['threshold']:
        actual_paid -= coupon['value']

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Create new order
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
    cursor.execute(sql, {'user_id':user_id,
                        'total': total,
                        'actual_paid': actual_paid,
                        'status': 200})
    # Retrive the newly inserted row
    cursor.execute('SELECT LAST_INSERT_ID()')
    order_id = cursor.fetchone()['LAST_INSERT_ID()']
    cart_items = get_items_by_user_id(user_id = user_id, scope = 'cart')
    update_sql = """UPDATE item SET
                    product_id = NULL,
                    product_name_snapshot = %(product_name_snapshot)s,
                    product_price_snapshot = %(product_price_snapshot)s
                    WHERE item_id = %(item_id)s"""
    for item in cart_items:
        cursor.execute(update_sql, {'product_name_snapshot': get_archive_index(item['product_name']),
                                    'product_price_snapshot': get_archive_index(item['price']),
                                    'item_id': item['item_id']})
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

    # Check is the input valid
    if not status.isdecimal():
        raise ValidationError('Invalid input type.')

    # Check for the existence of order
    order = find_order_by_id(order_id)
    if order is None:
        raise ValidationError('Order not found.')

    # Status code above or equal to 200 are normal orders
    # Status code below 200 are for deposites
    if (order['status'] - 200) * (int(status) - 200) < 0:
        raise ValidationError('Invalid status update.')

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

def get_order_details(order_id):
    # Return
    # Clean the input data
    user_id = str(user_id).strip()

    # Check for the existence of order
    order = find_order_by_id(order_id)
    if order is None:
        raise ValidationError('Order not found.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT order.order_id, product.product_name,
                FROM `order` WHERE user_id = %(user_id)s ORDER BY created_at DESC"""
    cursor.execute(sql, {'user_id': user_id})
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
    cursor.execute(sql, {'order_id': item_id})
    result = cursor.fetchone()
    return result
