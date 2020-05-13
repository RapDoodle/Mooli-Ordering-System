import datetime
from models.DAO import DAO
from utils.validation import is_money

def add_coupon(coupon_code, value, threshold, activate_date = None, expire_date = None):
    # Clean the input data
    coupon_code = str(coupon_code).strip()
    value = str(value).strip()
    threshold = str(threshold).strip()

    # Check is the input valid
    if not is_money(value):
        raise Exception('Invalid value.')
    if not is_money(threshold):
        raise Exception('Invalid threshold.')
    # TO-DO: Check for the validaty of time

    # Check the existence of the coupon
    if find_coupon(coupon_code) is not None:
        raise Exception('The coupon code already exists.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """INSERT INTO coupon (
        coupon_code,
        value,
        threshold,
        activate_date,
        expire_date
    ) VALUES (
        %(coupon_code)s,
        %(value)s,
        %(threshold)s,
        %(activate_date)s,
        %(expire_date)s
    )"""
    cursor.execute(sql, {'coupon_code': coupon_code,
                        'value': value,
                        'threshold': threshold,
                        'activate_date': activate_date,
                        'expire_date': expire_date})
    dao.commit()

def delete_coupon(coupon_code):
    # Clean the input data
    coupon_code = str(coupon_code).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check if the coupon exists
    if find_coupon(coupon_code) is None:
        raise Exception('The coupon does not exists.')

    sql = """DELETE FROM coupon WHERE coupon_code = %(coupon_code)s"""
    cursor.execute(sql, {'coupon_code': coupon_code})
    dao.commit()

def find_coupon(coupon_code):

    # Clean the input data
    coupon_code = str(coupon_code).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM coupon WHERE coupon_code = %(coupon_code)s"""
    cursor.execute(sql, {'coupon_code': coupon_code})
    result = cursor.fetchone()
    return result

def get_coupons(limit = 0, offset = 0):
    # Clean the input data
    limit = str(limit).strip()
    offset = str(offset).strip()

    if not limit.isdecimal() or not offset.isdecimal():
        raise Exception('Invalid input.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM coupon ORDER BY coupon_code ASC"""
    if not int(limit) == 0:
        sql += ' LIMIT ' + limit + ' OFFSET ' + offset
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
