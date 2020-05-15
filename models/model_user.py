import bcrypt
from models.DAO import DAO
from utils.exception import ValidationError
import utils.validation as validator

def add_user(username, email, password, first_name = '', last_name = '', gender = '', phone = '', is_staff = False):
    """The function creates a user based on the information provided
    It retuns the user_id if the user if created successfully.
    """
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
        raise ValidationError('Invalid username.')
    if not validator.is_valid_email(email):
        raise ValidationError('Invalid email.')
    if not validator.is_valid_password(password):
        raise ValidationError('Invalid password.')
    if not validator.is_valid_length(first_name, 0, 24):
        raise ValidationError('Invalid first name')
    if not validator.is_valid_length(last_name, 0, 24):
        raise ValidationError('Invalid last name')
    if gender not in ['M', 'F', '']:
        raise ValidationError('Invalid gender')
    if not isinstance(is_staff, bool):
        raise ValidationError('Invalid user type (customer or staff).')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    if find_user('username', username) is not None:
        raise ValidationError('The username was taken already.')

    password_hash = hash_password(password)

    sql = """INSERT INTO user(
                username,
                email,
                password_hash,
                first_name,
                last_name,
                gender,
                phone,
                is_staff
            ) VALUES (
                %(username)s,
                %(email)s,
                %(password_hash)s,
                %(first_name)s,
                %(last_name)s,
                %(gender)s,
                %(phone)s,
                %(is_staff)s
            )"""
    cursor.execute(sql, {'username': username,
                    'email': email,
                    'password_hash': password_hash,
                    'first_name': first_name,
                    'last_name': last_name,
                    'gender': gender,
                    'phone': phone,
                    'is_staff': is_staff
                    })
    dao.commit()

def update_user_info(user_id, first_name = '', last_name = '', gender = '', phone = ''):
    # Clean user input
    first_name = str(first_name).strip()
    last_name = str(last_name).strip()
    gender = str(gender).strip()
    phone = str(phone).strip()

    if not validator.is_valid_length(first_name, 0, 24):
        raise ValidationError('Invalid first name')
    if not validator.is_valid_length(last_name, 0, 24):
        raise ValidationError('Invalid last name')
    if gender not in ['M', 'F', '']:
        raise ValidationError('Invalid gender')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check the existence of the user
    sql = """SELECT * FROM user WHERE user_id = %(user_id)s"""
    cursor.execute(sql, {'user_id': user_id})
    result = cursor.fetchone()

    if result is None:
        raise ValidationError('User not found.')

    # Update information in the database
    sql = """UPDATE user SET
             first_name = %(first_name)s,
             last_name = %(last_name)s,
             gender = %(gender)s,
             phone = %(phone)s
             WHERE user_id = %(user_id)s"""
    cursor.execute(sql, {'first_name': first_name,
                         'last_name': last_name,
                         'gender': gender,
                         'phone': phone,
                         'user_id': user_id
                         })
    dao.commit()

def change_password(user_id, password):
    password = str(password).strip()

    if not validator.is_valid_password(password):
        raise ValidationError('Invalid password.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """SELECT * FROM user WHERE user_id = %(user_id)s"""
    cursor.execute(sql, {'user_id': user_id})
    result = cursor.fetchone()

    if result is None:
        raise ValidationError('User not found.')

    password_hash = hash_password(password)

    sql = """UPDATE user SET password_hash = %(password_hash)s
             WHERE user_id = %(user_id)s"""
    cursor.execute(sql, {'password_hash': password_hash,
                         'user_id': user_id})
    dao.commit()

def verify_credential(param, password, method = 'username'):
    # The function takes in username and password from user input
    # If the verification succeeded, the user's id will be returned
    # Otherwise, None will be returned

    # Check type of verification
    if method not in ['username', 'user_id']:
        raise ValidationError('Method not allowed.')

    # Clean the data
    param = str(param).strip()
    password = str(password).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query the database for password and user_id
    sql = ''
    if method == 'username':
        sql = """SELECT user_id, password_hash FROM user WHERE username = %(param)s"""
    else:
        sql = """SELECT user_id, password_hash FROM user WHERE user_id = %(param)s"""
    cursor.execute(sql, {'param': param})
    result = cursor.fetchone()

    if result is None:
        raise ValidationError('Invalid username')
    if not verify_password(password, result['password_hash']):
        raise ValidationError('Invalid password')
    return result['user_id']

def find_user(method, param):
    if method not in ['username', 'id']:
        raise ValidationError('Invalid method.')

    # Clean the input data
    param = str(param).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = ''
    if method == 'username':
        sql = """SELECT * FROM user WHERE username = %(param)s"""
    else:
        sql = """SELECT * FROM user WHERE user_id = %(param)s"""
    cursor.execute(sql, {'param': param})
    result = cursor.fetchone()
    return result

def verify_password(password, hashed_password):
    passwprd = str(password).strip()
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False

def hash_password(password):
    passwprd = str(password).strip()
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
