from models.DAO import DAO

def add_category(category_name, priority):
    # Clean the input data
    category_name = str(category_name).strip()
    priority = str(priority).strip()

    # Check is the input valid
    if not category_name or not priority.isdecimal():
        raise Exception('Invalid input type.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check if the category already exists
    if find_category('category_name', category_name) is not None:
        raise Exception('The category already exists.')

    sql = """INSERT INTO category (
        category_name,
        priority
    ) VALUES (
        %(category_name)s,
        %(priority)s
    )"""
    cursor.execute(sql, {'category_name': category_name, 'priority': priority})
    dao.commit()

def update_category(category_id, category_name, priority):
    # Clean the input data
    category_id = category_id.strip()
    category_name = category_name.strip()
    priority = priority.strip()

    # Check is the input valid
    if not category_name or not category_id or not priority.isdecimal():
        raise Exception('Invalid input type.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    if find_category('category_id', category_id) is None:
        raise Exception('The category does not exists.')

    sql = """UPDATE category SET category_name = %(category_name)s,
            priority = %(priority)s WHERE category_id = %(category_id)s"""
    cursor.execute(sql, {'category_name': category_name,
                        'priority': priority,
                        'category_id': category_id})
    dao.commit()

def remove_category(category_id):
    # Clean the input data
    category_id = str(category_id).strip()

    # Check is the input valid
    if not category_id.isdecimal():
        raise Exception('Invalid input type.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check if the category exists
    if find_category('category_id', category_id) is None:
        raise Exception('The category does not exists.')

    sql = """DELETE FROM category WHERE category_id = %(category_id)s"""
    cursor.execute(sql, {'category_id': category_id})
    dao.commit()

def find_category(method, param):
    # Check if the method is valid
    if method not in ['category_name', 'category_id']:
        raise Exception('Invalid method')

    # Clean the input data
    param = str(param).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = ''
    if method == 'category_name':
        sql = """SELECT * FROM category WHERE category_name = %(param)s"""
    else:
        sql = """SELECT * FROM category WHERE category_id = %(param)s"""
    cursor.execute(sql, {'param': param})
    result = cursor.fetchone()
    return result

def get_category_list():
    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM category ORDER BY priority DESC, category_name ASC"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
