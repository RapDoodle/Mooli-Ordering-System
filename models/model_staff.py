from models.DAO import DAO
from utils.validation import is_valid_length
from utils.exception import ValidationError
from models.shared import find_role, add_user

def add_staff(username, email, password, role_id, first_name = '', last_name = '', gender = '', phone = ''):
    # Call the add_user function in the user model
    user_id = add_user(username, email, password, first_name, last_name, gender, phone)

    # Clean user input
    role_id = str(role_id).strip()

    # Check if the role exists
    if find_role(role_id, 'role_id') is None:
        raise ValidationError('Invalid role.')

    # Check for the existence of the role
    role = find_role(role_id, 'role_id')
    if role is None:
        raise ValidationError('Invalid role.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """INSERT INTO staff (
                user_id,
                role_id
            ) VALUES (
                %(user_id)s,
                %(role_id)s
            )"""
    cursor.execute(sql, {'user_id': user_id, 'role_id': role_id})
    dao.commit()

    return user_id

def find_staff(param, method):
    """The function finds the staff according the staff's user_id or username

    The return dict contains: user_id, staff_id, and username
    """

    # Check if the method is valid
    if method not in ['staff_id', 'username']:
        raise ValidationError('Invalid method.')

    # Clean user input
    param = str(param).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query db for role
    sql = ''
    if method == 'staff_id':
        sql = """WITH s_u (user_id, username) AS (
                    SELECT user_id, username FROM user WHERE user_id = %(param)s
                )
                SELECT staff.user_id, staff.role_id, s_u.username FROM staff, s_u WHERE
                    staff.user_id = s_u.user_id"""
    else:
        sql = """WITH s_u (user_id, username) AS (
                    SELECT user_id, username FROM user WHERE username = %(param)s
                )
                SELECT staff.user_id, staff.role_id, s_u.username FROM staff, s_u WHERE
                    staff.user_id = s_u.user_id"""
    cursor.execute(sql, {'param': param})
    result = cursor.fetchone()

    return result
