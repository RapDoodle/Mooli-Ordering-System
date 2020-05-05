import utils.validation as validator
from models.DAO import DAO

def add_product(product_name, categories, price, priority, description = '', picture_uuid = '', thumbnail_uuid = ''):
    # Clean the input data
    product_name = product_name.strip()
    description = description.strip()
    price = price.strip()
    priority = priority.strip()
    description = description.strip()
    picture_uuid = picture_uuid.strip()
    thumbnail_uuid = thumbnail_uuid.strip()

    # Check is the input valid
    if (not product_name) or (not description) or (not priority.isdecimal()) or (type(categories) is not list):
        raise Exception('Invalid input type.')

    if not validator.is_money(price):
        raise Exception('Invalid pricing.')

    if len(categories) == 0:
        raise Exception('The product should belong to at least one category.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check if the item already exists
    if find_product('product_name', product_name) is not None:
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
    # Fetch the newly added id
    cursor.execute("""SELECT product_id FROM product WHERE product_name = %(product_name)s""",
            {'product_name': product_name})
    product_id = cursor.fetchone()['product_id']
    # Create relationship between product and category
    sql = """INSERT INTO product_category(product_id, category_id) VALUES (
            %(product_id)s,
            %(category_id)s
    )"""
    for category_id in categories:
        cursor.execute(sql, {'product_id': product_id, 'category_id': category_id})

    dao.commit()

def update_product(product_id, product_name, categories, price, priority, description, picture_uuid, thumbnail_uuid):
    # Clean the input data
    product_id = product_id.strip()
    product_name = product_name.strip()
    description = description.strip()
    price = price.strip()
    priority = priority.strip()
    description = description.strip()
    picture_uuid = picture_uuid.strip()
    thumbnail_uuid = thumbnail_uuid.strip()

    # Check is the input valid
    if (not product_id) or (not product_name) or (not description) or (not priority.isdecimal()) or (type(categories) is not list):
        raise Exception('Invalid input type.')

    if not validator.is_money(price):
        raise Exception('Invalid pricing.')

    if len(categories) == 0:
        raise Exception('The product should belong to at least one category.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check if the item exists
    if find_product('product_name', product_name) is None:
        raise Exception('The category does not exists.')

    sql = """UPDATE product SET
            product_name = %(product_name)s,
            description = %(description)s,
            price = %(price)s,
            thumbnail_uuid = %(thumbnail_uuid)s,
            picture_uuid = %(picture_uuid)s,
            priority = %(priority)s
            WHERE product_id = %(product_id)s
    """
    cursor.execute(sql, {'product_name': product_name,
                        'description': description,
                        'priority': priority,
                        'price': price,
                        'thumbnail_uuid': thumbnail_uuid,
                        'picture_uuid': picture_uuid,
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
    product_id = product_id.strip()

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
    if method not in ['category_name', 'all']:
        raise Exception('Invalid method')
    # Clean the input data
    param = param.strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = ''
    if method == 'category_name':
        if not param:
            raise Exception('The parameter can not be empty.')
        sql = """SELECT * FROM product, product_category, category
                 WHERE product.product_id = product_category.product_id
                    AND product_category.category_id = category.category_id
                    AND category.category_name = %(param)s
                 ORDER BY product.priority DESC, product.product_name ASC"""
        cursor.execute(sql, {'param': param})
    else:
        sql = """SELECT * FROM product ORDER BY product.priority DESC, product.product_name ASC"""
        cursor.execute(sql)
    result = cursor.fetchall()
    return result

def find_product(method, param):
    if method not in ['product_name', 'product_id']:
        raise Exception('Invalid method.')
    # Clean the input data
    param = param.strip()

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
