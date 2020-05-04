import re
from models.DAO import DAO

def add_product(product_name, categories, price, priority, description = '', picture_uuid = '', thumbnail_uuid = ''):
    # Clean the input data
    product_name = product_name.strip()
    description = description.strip()
    price = price.strip()

    # Check is the input valid
    if (not product_name) or (not description) or (not priority.isdecimal()) or (type(categories) is not list):
        raise Exception('Invalid input type.')

    verify_price_regex = re.compile('^[0-9]+(\.[0-9]{1,2})?$')
    if verify_price_regex.match(price) is None:
        raise Exception('Invalid pricing.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check if the item already exists
    if find_product_by_name(product_name) is not None:
        raise Exception('The category already exists.')

    sql = """INSERT INTO product (
        product_name,
        description,
        price,
        thumbnail_uuid,
        picture_uuid,
        priority
    ) VALUES (
        %(product_name)s,
        %(description)s,
        %(price)s,
        %(thumbnail_uuid)s,
        %(picture_uuid)s,
        %(priority)s
    )"""
    cursor.execute(sql, {'product_name': product_name,
                        'description': description,
                        'priority': priority,
                        'price': price,
                        'thumbnail_uuid': thumbnail_uuid,
                        'picture_uuid': picture_uuid,
                        })
    dao.commit()

def update_product():
    pass

def remove_product():
    pass

def get_products_by_category(category):
    pass

def find_product_by_name(product_name):
    # Clean the input data
    product_name = product_name.strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM product WHERE product_name = %(product_name)s"""
    cursor.execute(sql, {'product_name': product_name})
    result = cursor.fetchone()
    return result
