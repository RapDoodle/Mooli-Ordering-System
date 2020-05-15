import utils.validation as validator
from models.DAO import DAO
from utils.exception import ValidationError
from models.shared import find_user, find_product

def add_item(user_id, product_id, amount):
    # Clean the input data
    user_id = str(user_id).strip()
    product_id = str(product_id).strip()
    amount = str(amount).strip()

    # Check is the input valid
    if not user_id or not product_id or not amount.isdecimal():
        raise ValidationError('Invalid input type.')

    # Check for the existence of user and product
    if find_user(method = 'id', param = user_id) is None:
        raise ValidationError('Invalid user id.')
    if find_product(method = 'product_id', param = product_id) is None:
        raise ValidationError('Invalid product.')

    # Check the user's cart. If the item already exists, perform update instead of amount
    item = find_cart_item_id(user_id, product_id)
    if item is not None:
        return update_item_amount(item['item_id'], int(item['amount']) + int(amount))

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """INSERT INTO item (
        user_id,
        product_id,
        amount
    ) VALUES (
        %(user_id)s,
        %(product_id)s,
        %(amount)s
    )"""
    cursor.execute(sql, {'user_id': user_id,
                        'product_id': product_id,
                        'amount': amount})
    dao.commit()

def update_item_amount(item_id, amount):
    # The function only changes the amount, not the item_id and product_id!!
    # Clean the input data
    item_id = str(item_id).strip()
    amount = str(amount).strip()

    # Check is the input valid
    if not amount.isdecimal():
        raise ValidationError('Invalid input type.')

    # Check for the existence of item
    cart_item = find_cart_item_by_id(item_id)
    if cart_item is None:
        raise ValidationError('Cart item not found.')
    if cart_item['order_id'] is not None:
        raise ValidationError('Orderd item can not be altered.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """UPDATE item SET
            amount = %(amount)s
            WHERE item_id = %(item_id)s"""
    cursor.execute(sql, {'amount': amount,
                        'item_id': item_id})
    dao.commit()

def remove_item(item_id):
    # Clean the input data
    item_id = str(item_id).strip()

    # Check for existence
    if find_cart_item_by_id(item_id) is None:
        raise ValidationError('Item not found.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """DELETE FROM item WHERE item_id = %(item_id)s"""
    cursor.execute(sql, {'item_id': item_id})

    dao.commit()

def get_items_by_user_id(user_id, scope):
    if scope not in ['cart', 'purchased', 'all']:
        raise ValidationError('Unknown method.')

    # Clean the input data
    user_id = str(user_id).strip()

    # Check for the existence of user
    if find_user(method = 'id', param = user_id) is None:
        raise ValidationError('Invalid user id.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT item.item_id,
                    item.product_id,
                    product.product_name,
                    product.price,
                    item.amount
             FROM item, product WHERE
                item.product_id = product.product_id AND
                user_id = %(user_id)s"""
    if scope == 'cart':
        sql += """ AND item.order_id IS NULL"""
    elif scope == 'purchased':
        sql += """ AND item.order_id IS NOT NULL"""
    sql += """ ORDER BY created_at DESC"""
    cursor.execute(sql, {'user_id': user_id})
    result = cursor.fetchall()
    return result

def find_cart_item_id(user_id, product_id):
    # NOTE: Cart items are items that are not purchased (without order_id)
    # Clean the input data
    user_id = str(user_id).strip()
    product_id = str(product_id).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM item WHERE
                user_id = %(user_id)s AND
                product_id = %(product_id)s AND
                order_id IS NULL"""
    cursor.execute(sql, {'user_id': user_id,
                        'product_id': product_id})
    result = cursor.fetchone()
    return result

def find_cart_item_by_id(item_id):
    # Clean the input data
    item_id = str(item_id).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM item WHERE
                item_id = %(item_id)s"""
    cursor.execute(sql, {'item_id': item_id})
    result = cursor.fetchone()
    return result
