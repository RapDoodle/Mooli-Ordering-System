from models.DAO import DAO
import utils.validation as validator
import models.model_user as user_common

def add_customer(username, email, password, first_name = '', last_name = '', gender = '', phone = ''):
    # clean the data
    username = username.strip()
    email = email.strip()
    password = password.strip()
    first_name = first_name.strip()
    last_name = last_name.strip()
    gender = gender.strip()
    phone = phone.strip()

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

    if find_user('username', username) is not None:
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

def change_password(customer_id, password):
    password = password.strip()

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

def verify_credential(username, password):
    # The function takes in username and password from user input
    # If the verification succeeded, the user's id will be returned
    # Otherwise, None will be returned

    # Clean the data
    username = username.strip()
    password = password.strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query the database for password and customer_id
    sql = """SELECT customer_id, password_hash FROM customer WHERE username = %(username)s ORDER BY customer_id"""
    cursor.execute(sql, {'username': username})
    result = cursor.fetchone()
    if result is None:
        raise Exception('Invalid username or password')
    if not user_common.verify_password(password, result['password_hash']):
        raise Exception('Invalid username or password')
    return result['customer_id']

def find_user(method, param):
    if method not in ['username', 'id']:
        raise Exception('Invalid method.')
    # Clean the input data
    param = param.strip()

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
