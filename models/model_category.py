from models.DAO import DAO

def add_category(category_name, priorty):
    # Clean the input data
    category_name = category_name.strip()
    priorty = priorty.strip()

    # Check is the input valid
    if not category_name or not priorty.isdecimal():
        raise Exception('Invalid input type.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check if the ccategory already exists

    sql = """INSERT INTO category (
        category_name,
        priority
    ) VALUES (
        %(category_name)s,
        %(priorty)s
    )"""
    cursor.execute(sql, {'category_name': category_name, 'priorty': priorty})
    dao.commit()

def remove_category(category_name):
    pass

def find_category_by_name(category_name):
    # Clean the input data
    category_name = category_name.strip()
    priorty = priorty.strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM category WHERE category_name = %(category_name)s"""
    cursor.execute()
    result = cursor.fetchone()

    return result
