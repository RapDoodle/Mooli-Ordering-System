from models.DAO import DAO
import utils.validation as validator
import models.model_user as user_common

def add_customer(username, email, password, first_name = '', last_name = '', gender = '', phone = ''):
    # clean the data
    username = str(username).strip()
    email = str(email).strip()
    password = str(password).strip()
    first_name = str(first_name).strip()
    last_name = str(last_name).strip()
    gender = str(gender).strip()
    phone = str(phone).strip()

    # Verify user input
    if not validator.is_valid_username(username):
        raise Exception('Invalid username.')
    if not validator.is_valid_email(email):
        raise Exception('Invalid email.')
    if not validator.is_valid_password(password):
        raise Exception('Invalid password.')
    if not validator.is_valid_length(first_name, 0, 24):
        raise Exception('Invalid first name')
    if not validator.is_valid_length(last_name, 0, 24):
        raise Exception('Invalid last name')
    if gender not in ['M', 'F', '']:
        raise Exception('Invalid gender')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    if find_customer('username', username) is not None:
        raise Exception('The username was taken already.')

    password_hash = user_common.hash_password(password)

    sql = """INSERT INTO customer(
                username,
                email,
                password_hash,
                first_name,
                last_name,
                gender,
                phone
            ) VALUES (
                %(username)s,
                %(email)s,
                %(password_hash)s,
                %(first_name)s,
                %(last_name)s,
                %(gender)s,
                %(phone)s
            )"""
    cursor.execute(sql, {'username': username,
                    'email': email,
                    'password_hash': password_hash,
                    'first_name': first_name,
                    'last_name': last_name,
                    'gender': gender,
                    'phone': phone
                    })
    dao.commit()

def update_customer_info(customer_id, first_name = '', last_name = '', gender = '', phone = ''):
    # Clean user input
    first_name = str(first_name).strip()
    last_name = str(last_name).strip()
    gender = str(gender).strip()
    phone = str(phone).strip()

    if not validator.is_valid_length(first_name, 0, 24):
        raise Exception('Invalid first name')
    if not validator.is_valid_length(last_name, 0, 24):
        raise Exception('Invalid last name')
    if gender not in ['M', 'F', '']:
        raise Exception('Invalid gender')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check the existence of the customer
    sql = """SELECT * FROM customer WHERE customer_id = %(customer_id)s"""
    cursor.execute(sql, {'customer_id': customer_id})
    result = cursor.fetchone()

    if result is None:
        raise Exception('User not found.')

    # Update information in the database
    sql = """UPDATE customer SET
             first_name = %(first_name)s,
             last_name = %(last_name)s,
             gender = %(gender)s,
             phone = %(phone)s
             WHERE customer_id = %(customer_id)s"""
    cursor.execute(sql, {'first_name': first_name,
                         'last_name': last_name,
                         'gender': gender,
                         'phone': phone,
                         'customer_id': customer_id
                         })
    dao.commit()

def change_password(customer_id, password):
    password = str(password).strip()

    if not validator.is_valid_password(password):
        raise Exception('Invalid password.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """SELECT * FROM customer WHERE customer_id = %(customer_id)s"""
    cursor.execute(sql, {'customer_id': customer_id})
    result = cursor.fetchone()

    if result is None:
        raise Exception('User not found.')

    password_hash = user_common.hash_password(password)

    sql = """UPDATE customer SET password_hash = %(password_hash)s
             WHERE customer_id = %(customer_id)s"""
    cursor.execute(sql, {'password_hash': password_hash,
                         'customer_id': customer_id})
    dao.commit()

def verify_credential(param, password, method = 'username'):
    # The function takes in username and password from user input
    # If the verification succeeded, the user's id will be returned
    # Otherwise, None will be returned

    # Check type of verification
    if method not in ['username', 'customer_id']:
        raise Exception('Method not allowed.')

    # Clean the data
    param = str(param).strip()
    password = str(password).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query the database for password and customer_id
    sql = ''
    if method == 'username':
        sql = """SELECT customer_id, password_hash FROM customer WHERE username = %(param)s"""
    else:
        sql = """SELECT customer_id, password_hash FROM customer WHERE customer_id = %(param)s"""
    cursor.execute(sql, {'param': param})
    result = cursor.fetchone()

    if result is None:
        raise Exception('Invalid username')
    if not user_common.verify_password(password, result['password_hash']):
        raise Exception('Invalid password')
    return result['customer_id']

def find_customer(method, param):
    if method not in ['username', 'id']:
        raise Exception('Invalid method.')

    # Clean the input data
    param = str(param).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = ''
    if method == 'username':
        sql = """SELECT * FROM customer WHERE username = %(param)s"""
    else:
        sql = """SELECT * FROM customer WHERE customer_id = %(param)s"""
    cursor.execute(sql, {'param': param})
    result = cursor.fetchone()
    return result
