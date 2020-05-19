import utils.validation as validator
from models.DAO import DAO
from utils.exception import ValidationError
from models.shared import get_product_ratings
import models.FS as fs
import os

def add_product(product_name, categories, price, priority, description = ''):
    # Clean the input data
    product_name = str(product_name).strip()
    description = str(description).strip()
    price = str(price).strip()
    priority = str(priority).strip()
    description = str(description).strip()

    # Check is the input valid
    if (not product_name) or (not description) or (not priority.isdecimal()) or (type(categories) is not list):
        raise ValidationError('Invalid input type.')

    if not validator.is_money(price):
        raise ValidationError('Invalid pricing.')

    if len(categories) == 0:
        raise ValidationError('The product should belong to at least one category.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check if the item already exists
    if find_product('product_name', product_name) is not None:
        raise ValidationError('The product already exists.')

    sql = """INSERT INTO product (
        product_name,
        description,
        price,
        priority
    ) VALUES (
        %(product_name)s,
        %(description)s,
        %(price)s,
        %(priority)s
    )"""
    cursor.execute(sql, {'product_name': product_name,
                        'description': description,
                        'priority': priority,
                        'price': price
                        })

    # Fetch the newly added id
    cursor.execute("""SELECT product_id FROM product WHERE product_name = %(product_name)s""",
            {'product_name': product_name})
    cursor.execute('SELECT LAST_INSERT_ID()')
    product_id = cursor.fetchone()['LAST_INSERT_ID()']

    # Create relationship between product and category
    sql = """INSERT INTO product_category(product_id, category_id) VALUES (
            %(product_id)s,
            %(category_id)s
    )"""
    for category_id in categories:
        cursor.execute(sql, {'product_id': product_id, 'category_id': category_id})

    dao.commit()

def update_product(product_id, product_name, categories, price, priority, description=''):
    # Clean the input data
    product_id = str(product_id).strip()
    product_name = str(product_name).strip()
    description = str(description).strip()
    price = str(price).strip()
    priority = str(priority).strip()
    description = str(description).strip()

    # Check is the input valid
    if (not product_id) or (not product_name) or (not description) or (not priority.isdecimal()) or (type(categories) is not list):
        raise ValidationError('Invalid input type.')

    if not validator.is_money(price):
        raise ValidationError('Invalid pricing.')

    if len(categories) == 0:
        raise ValidationError('The product should belong to at least one category.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check if the item exists
    if find_product('product_name', product_name) is None:
        raise ValidationError('The category does not exists.')

    sql = """UPDATE product SET
            product_name = %(product_name)s,
            description = %(description)s,
            price = %(price)s,
            priority = %(priority)s
            WHERE product_id = %(product_id)s
    """
    cursor.execute(sql, {'product_name': product_name,
                        'description': description,
                        'priority': priority,
                        'price': price,
                        'product_id': product_id
                        })

    # Create relationship between product and category
    sql = """DELETE FROM product_category WHERE product_id = %(product_id)s"""
    cursor.execute(sql, {'product_id': product_id})
    sql = """INSERT INTO product_category(product_id, category_id) VALUES (
            %(product_id)s,
            %(category_id)s
    )"""
    for category_id in categories:
        cursor.execute(sql, {'product_id': product_id, 'category_id': category_id})

    dao.commit()

def remove_product(product_id):
    # Clean the input data
    product_id = str(product_id).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Clear from the product_category table
    sql = """DELETE FROM product_category WHERE product_id = %(product_id)s"""
    cursor.execute(sql, {'product_id': product_id})
    # Clear from the products table
    sql = """DELETE FROM product WHERE product_id = %(product_id)s"""
    cursor.execute(sql, {'product_id': product_id})

    dao.commit()

def get_products(method, param = ''):
    if method not in ['category_id', 'all']:
        raise ValidationError('Invalid method')
    # Clean the input data
    param = str(param).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = ''
    if method == 'category_id':
        if not param:
            raise ValidationError('The parameter can not be empty.')
        sql = """SELECT * FROM product, product_category, category
                 WHERE product.product_id = product_category.product_id
                    AND product_category.category_id = category.category_id
                    AND category.category_id = %(param)s
                 ORDER BY product.priority DESC, product.product_name ASC"""
        cursor.execute(sql, {'param': param})
    else:
        sql = """SELECT * FROM product ORDER BY product.priority DESC, product.product_name ASC"""
        cursor.execute(sql)
    result = cursor.fetchall()

    for product in result:
        product['rating'] = get_product_ratings(product['product_id'])

    return result

def find_product(method, param):
    if method not in ['product_name', 'product_id']:
        raise ValidationError('Invalid method.')
    # Clean the input data
    param = str(param).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = ''
    if method == 'product_name':
        sql = """SELECT * FROM product WHERE product_name = %(param)s"""
    else:
        sql = """SELECT * FROM product WHERE product_id = %(param)s"""
    cursor.execute(sql, {'param': param})
    result = cursor.fetchone()

    return result

def update_image(product_id, update_type, f):
    """The function takes in an image and save it to the file system

    Parameters:
    product_id -- the id of the product
    update_type -- the type of the update
                1 - picture
                2 - thumbnail
    f -- the image file
    """
    # Verify the type
    update_type = str(update_type).strip()
    if update_type not in ['1', '2']:
        raise ValidationError('Invalid update type.')

    # Verify the file
    f.seek(0, os.SEEK_END)
    if f.tell() == 0:
        raise ValidationError('Empty file.')

    # Clean the input data
    product_id = str(product_id).strip()

    # Verify the existence of the file
    if find_product('product_id', product_id) is None:
        raise ValidationError('The product does not exists.')

    print(type(f))
    if update_type == '1':
        fs.save_picture(product_id, f)
    else:
        fs.save_thumbnail(product_id, f)
