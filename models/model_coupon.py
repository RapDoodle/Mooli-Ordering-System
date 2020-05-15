import datetime as dt
from models.DAO import DAO
from utils.exception import ValidationError
from utils.validation import is_money

def add_coupon(coupon_code, value, threshold, activate_date = None, expire_date = None):
    # Clean the input data
    coupon_code = str(coupon_code).strip()
    value = str(value).strip()
    threshold = str(threshold).strip()

    # Check is the input valid
    if not is_money(value):
        raise ValidationError('Invalid value.')
    if not is_money(threshold):
        raise ValidationError('Invalid threshold.')
    # TO-DO: Check for the validaty of time

    # Check the existence of the coupon
    if find_coupon(coupon_code) is not None:
        raise ValidationError('The coupon code already exists.')

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
        raise ValidationError('The coupon does not exists.')

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
        raise ValidationError('Invalid input.')

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

def find_coupon_and_check_validity(coupon_code):
    # Data clearning is guaranteened to happen within find_coupon
    coupon = find_coupon(coupon_code)

    if coupon is not None:
        # Check if the coupon is active or has expired
        current_time = dt.datetime.now()
        activate_date = coupon['activate_date'] if coupon['activate_date'] is not None else dt.datetime(1970, 1, 1)
        expire_date = coupon['expire_date'] if coupon['expire_date'] is not None else dt.datetime(9999, 12, 31)
        if (current_time - activate_date).total_seconds() < 0:
            raise ValidationError('The coupon is not activate yet.')
        elif (expire_date - current_time).total_seconds() < 0:
            raise ValidationError('The coupon has expired.')

    return coupon
