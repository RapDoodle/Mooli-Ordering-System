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

def update_staff(user_id, role_id, first_name = '', last_name = '', gender = '', phone = ''):
    # Call the add staff function
    from models.model_user import update_user_info
    update_user_info(
        user_id = user_id,
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        phone = phone
    )

    # Clean user input
    role_id = str(role_id).strip()

    # Check if the staff exists
    if find_staff(user_id, 'user_id') is None:
        raise ValidationError('Staff not found.')

    # Check if the role exists
    if find_role(role_id, 'role_id') is None:
        raise ValidationError('Invalid role.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """UPDATE staff SET role_id = %(role_id)s WHERE user_id = %(user_id)s"""
    cursor.execute(sql, {'role_id': role_id, 'user_id': user_id})
    
    dao.commit()

def delete_staff(user_id):
    # Clean user input
    user_id = str(user_id).strip()

    # Check if the staff exists
    if find_staff(user_id, 'user_id') is None:
        raise ValidationError('Staff not found.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check the number of staff in the system
    sql = """SELECT COUNT(user_id) AS cnt FROM staff"""
    cursor.execute(sql)
    result = cursor.fetchone()['cnt']

    if result <= 1:
        raise ValidationError('The system only has one staff. Deleting the staff will result in the system inaccessible from the staff end.')

    sql = """UPDATE staff SET role_id = %(role_id)s WHERE user_id = %(user_id)s"""
    cursor.execute(sql, {'role_id': role_id, 'user_id': user_id})
    
    dao.commit()

def find_staff(param, method):
    """The function finds the staff according the staff's user_id or username

    The return dict contains: user_id and username
    """
    # Check if the method is valid
    if method not in ['user_id', 'username']:
        raise ValidationError('Invalid method.')

    # Clean user input
    param = str(param).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query db for role
    sql = ''
    if method == 'user_id':
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

def get_staff_list():
    """The function returns all the complete table of information for staff"""
    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query db for role
    sql = """SELECT * FROM staff, role, user WHERE
                staff.user_id = user.user_id AND
                staff.role_id = role.role_id"""
    cursor.execute(sql)
    result = cursor.fetchall()

    return result

def authorization_check(user_id, permission_name):
    """The function verifies if the staff is authorized for the permission

    Parameters:
    user_id -- the user_id of the staff
    permission_name -- the name of the permission
    """
    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query db for role
    # Check if the user is a superadmin
    sql = """SELECT role_name FROM staff, role WHERE
                staff.user_id = %(user_id)s AND
                staff.role_id = role.role_id AND
                role.role_name = 'superadmin'"""
    cursor.execute(sql, {'user_id': user_id, 'permission_name': permission_name})
    result = cursor.fetchone()
    if result is not None:
        return True

    # The staff is not a superuser, check for permission
    sql = """SELECT permission_name FROM staff, role_permission, permission WHERE
                staff.user_id = %(user_id)s AND
                staff.role_id = role_permission.role_id AND
                role_permission.permission_id = permission.permission_id AND
                permission.permission_name = %(permission_name)s"""
    cursor.execute(sql, {'user_id': user_id, 'permission_name': permission_name})
    result = cursor.fetchone()

    return False if result is None else True