from models.DAO import DAO
from models.shared import get_items_by_user_id, find_user, find_coupon_and_check_validity

def place_order(user_id, coupon_code = ''):
    # Clean the input data
    user_id = str(user_id).strip()
    coupon_code = str(coupon_code).strip()

    # Retrive coupon data
    coupon = find_coupon_and_check_validity(coupon_code)

    # If the user did input a coupon but the coupon is invalid
    if len(coupon_code) > 0 and coupon is None:
        raise Exception('Invalid coupon code.')

    # Check for the existence of user
    if find_user(method = 'id', param = user_id) is None:
        raise Exception('Invalid user id.')

    # Check the user's cart. If the item already exists, perform update instead of amount
    items = get_items_by_user_id(user_id = user_id, scope = 'cart')
    if len(items) == 0:
        raise Exception('No item found in cart.')

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

    sql = """INSERT INTO `order` (
        total,
        actual_paid,
        status
    ) VALUES (
        %(total)s,
        %(actual_paid)s,
        %(status)s
    )"""
    cursor.execute(sql, {'total': total,
                        'actual_paid': actual_paid,
                        'status': 0})
    dao.commit()

# def update_item_amount(item_id, amount):
#     # The function only changes the amount, not the item_id and product_id!!
#     # Clean the input data
#     item_id = str(item_id).strip()
#     amount = str(amount).strip()
#
#     # Check is the input valid
#     if not amount.isdecimal():
#         raise Exception('Invalid input type.')
#
#     # Check for the existence of item
#     cart_item = find_item_by_id(item_id)
#     if cart_item is None:
#         raise Exception('Cart item not found.')
#     if cart_item['order_id'] is not None:
#         raise Exception('Orderd item can not be altered.')
#
#     # Establish db connection
#     dao = DAO()
#     cursor = dao.cursor()
#
#     sql = """UPDATE item SET
#             amount = %(amount)s
#             WHERE item_id = %(item_id)s"""
#     cursor.execute(sql, {'amount': amount,
#                         'item_id': item_id})
#     dao.commit()
#
# def remove_item(item_id):
#     # Clean the input data
#     item_id = str(item_id).strip()
#
#     # Check for existence
#     if find_item_by_id(item_id) is None:
#         raise Exception('Item not found.')
#
#     # Establish db connection
#     dao = DAO()
#     cursor = dao.cursor()
#
#     sql = """DELETE FROM item WHERE item_id = %(item_id)s"""
#     cursor.execute(sql, {'item_id': item_id})
#
#     dao.commit()
#
# def get_items_by_user_id(user_id, scope):
#     if scope not in ['cart', 'purchased', 'all']:
#         raise Exception('Unknown method.')
#
#     # Clean the input data
#     user_id = str(user_id).strip()
#
#     # Check for the existence of user
#     if find_user(method = 'id', param = user_id) is None:
#         raise Exception('Invalid user id.')
#
#     # Establish db connection
#     dao = DAO()
#     cursor = dao.cursor()
#
#     # Query database
#     sql = ''
#     if scope == 'cart':
#         sql = """SELECT * FROM item WHERE
#                 user_id = %(user_id)s AND
#                 order_id IS NULL
#                 ORDER BY created_at DESC"""
#     elif scope == 'purchased':
#         sql = """SELECT * FROM item WHERE
#                 user_id = %(user_id)s AND
#                 order_id IS NOT NULL
#                 ORDER BY created_at DESC"""
#     else:
#         # Case: all
#         sql = """SELECT * FROM item WHERE
#                 user_id = %(user_id)s
#                 ORDER BY created_at DESC"""
#     cursor.execute(sql, {'user_id': user_id})
#     result = cursor.fetchall()
#     return result
#
# def find_cart_item_id(user_id, product_id):
#     # NOTE: Cart items are items that are not purchased (without order_id)
#     # Clean the input data
#     user_id = str(user_id).strip()
#     product_id = str(product_id).strip()
#
#     # Establish db connection
#     dao = DAO()
#     cursor = dao.cursor()
#
#     # Query database
#     sql = """SELECT * FROM item WHERE
#                 user_id = %(user_id)s AND
#                 product_id = %(product_id)s AND
#                 order_id IS NULL"""
#     cursor.execute(sql, {'user_id': user_id,
#                         'product_id': product_id})
#     result = cursor.fetchone()
#     return result
#
# def find_item_by_id(item_id):
#     # Clean the input data
#     item_id = str(item_id).strip()
#
#     # Establish db connection
#     dao = DAO()
#     cursor = dao.cursor()
#
#     # Query database
#     sql = """SELECT * FROM item WHERE
#                 item_id = %(item_id)s"""
#     cursor.execute(sql, {'item_id': item_id})
#     result = cursor.fetchone()
#     return result
