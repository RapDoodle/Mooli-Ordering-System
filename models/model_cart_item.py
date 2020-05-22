import utils.validation as validator
from models.DAO import DAO
from utils.exception import ValidationError
from models.shared import find_user, find_product

def create_cart_item(user_id, product_id, amount = 1):
    """The function creates a cart item if the cart item does not exist.
    Otherwise, the cart item will be updated in an "append" manner
    """
    # Clean the input data
    user_id = str(user_id).strip()
    product_id = str(product_id).strip()
    amount = str(amount).strip()

    # Check is the input valid
    if not user_id or not product_id:
        raise ValidationError('Invalid identifier(s).')
    if not amount.isdecimal():
        raise ValidationError('Invalid amount.')

    # Check for the existence of user and product
    if find_user(method = 'id', param = user_id) is None:
        raise ValidationError('Invalid user id.')
    if find_product(method = 'product_id', param = product_id) is None:
        raise ValidationError('Invalid product id.')

    # Check the user's cart. If the item already exists, perform update instead of insertion
    item = find_cart_item_id(user_id, product_id)
    if item is not None:
        return update_cart_item_amount(item['cart_item_id'], int(item['amount']) + int(amount))

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """INSERT INTO cart_item (
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

def update_cart_item_amount(cart_item_id, amount):
    """The function will set the item's amount attribute to the given paramter amount
    The function only changes the amount, not the cart_item_id and product_id!!
    """
    # Clean the input data
    cart_item_id = str(cart_item_id).strip()
    amount = str(amount).strip()

    # Check is the input valid
    if not amount.isdecimal():
        raise ValidationError('Invalid amount.')

    # If the amount less than or equal to 0, delete the cart item
    if int(amount) <= 0:
        return delete_cart_item(cart_item_id)

    # Check for the existence of item
    cart_item = find_cart_item_by_id(cart_item_id)
    if cart_item is None:
        raise ValidationError('The given cart item does not exists.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """UPDATE cart_item SET
            amount = %(amount)s
            WHERE cart_item_id = %(cart_item_id)s"""
    cursor.execute(sql, {'amount': amount,
                        'cart_item_id': cart_item_id})
    dao.commit()

def delete_cart_item(cart_item_id, relay_dao = None):
    """The function finds a cart item according to its id"""
    # Clean the input data
    cart_item_id = str(cart_item_id).strip()

    # Check for existence
    if find_cart_item_by_id(cart_item_id) is None:
        raise ValidationError('The given cart item does not exists.')

    # Establish db connection
    if relay_dao is None:  
        dao = DAO()
        cursor = dao.cursor()
    else:
        cursor = relay_dao.cursor()

    sql = """DELETE FROM cart_item WHERE cart_item_id = %(cart_item_id)s"""
    cursor.execute(sql, {'cart_item_id': cart_item_id})

    # Only commit when the operation is considered atomic
    if relay_dao is None:
        dao.commit()

def find_cart_item_by_id(cart_item_id):
    # Clean the input data
    cart_item_id = str(cart_item_id).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM cart_item WHERE
                cart_item_id = %(cart_item_id)s"""
    cursor.execute(sql, {'cart_item_id': cart_item_id})
    result = cursor.fetchone()
    return result

def find_cart_item_id(user_id, product_id):
    """The function returns a cart item according to the id of the cart item
        and a product it
    """
    # Clean the input data
    user_id = str(user_id).strip()
    product_id = str(product_id).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM cart_item WHERE
                user_id = %(user_id)s AND
                product_id = %(product_id)s"""
    cursor.execute(sql, {'user_id': user_id,
                        'product_id': product_id})
    result = cursor.fetchone()
    return result

def get_cart_items_by_user_id(user_id):
    """The function find all the items in the user's cart and return the info
        required by the front-end

    Keyword arguments:
    user_id -- the user id
    """
    # Clean the input data
    user_id = str(user_id).strip()

    # Check for the existence of user
    if find_user(param = user_id, method = 'id') is None:
        raise ValidationError('Invalid user id.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT cart_item.cart_item_id,
                    cart_item.product_id,
                    product.product_name,
                    product.price,
                    cart_item.amount
             FROM cart_item, product WHERE
                cart_item.product_id = product.product_id AND
                user_id = %(user_id)s ORDER BY created_at DESC"""
    cursor.execute(sql, {'user_id': user_id})
    result = cursor.fetchall()
    return result
