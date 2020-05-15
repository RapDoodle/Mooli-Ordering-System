from models.DAO import DAO
from utils.validation import is_valid_length
from utils.exception import ValidationError

def add_role(role_name, permission_ids):
    # Clean user input
    role_name = str(role_name).strip()

    if not isinstance(permission_ids, list):
        raise ValidationError('Permission IDs passed incorrectly.')

    # Check is the role_name withn valid length
    if not is_valid_length(role_name, 1, 32):
        raise ValidationError('Invalid length for role name.')

    # Check if the role already exists
    role = find_role(role_name, 'role_name')
    if role is not None:
        raise ValidationError('The role already exists.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """INSERT INTO role (role_name) VALUES (%(role_name)s)"""
    cursor.execute(sql, {'role_name': role_name})

    # Fetch the id of the newly inserted role
    cursor.execute('SELECT LAST_INSERT_ID()')
    role_id = cursor.fetchone()['LAST_INSERT_ID()']

    dao.commit()

    # Set the role's permission
    set_role_permissions(role_id, permission_ids)

    return role_id

def find_role(param, method):
    """The function will find the role according to the method specified and the
    given parameter.

    Methods include 'role_id' and 'role_name'
    """
    # Check if the method is valid
    if method not in ['role_id', 'role_name']:
        raise ValidationError('Invalid method.')

    # Clean user input
    param = str(param).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query db for role
    sql = """SELECT * FROM role WHERE """
    sql += method
    sql += """ = %(param)s"""
    cursor.execute(sql, {'param': param})
    result = cursor.fetchone()

    return result

def get_all_roles():
    """The function will return all the roles in the database"""
    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query db for role
    sql = """SELECT * FROM role ORDER BY role_name ASC"""
    cursor.execute(sql)
    result = cursor.fetchall()

    if result is None:
        return []

    return result

def update_role(role_id, role_name, permission_ids):
    """The function set's the role_name of the given row (by role_id)"""
    # Clean user input
    role_id = str(role_id).strip()
    role_name = str(role_name).strip()

    if not isinstance(permission_ids, list):
        raise ValidationError('Permission IDs passed incorrectly.')

    # Check is the role_name withn valid length
    if not is_valid_length(role_name, 1, 32):
        raise ValidationError('Invalid length for role name.')

    # Check if the role already exists
    role = find_role(role_name, 'role_name')
    if role is not None:
        raise ValidationError('The role already exists.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """UPDATE role SET role_name =  %(role_name)s WHERE role_id = %(role_id)s"""
    cursor.execute(sql, {'role_name': role_name, 'role_id': role_id})

    dao.commit()

    # Set the role's permission
    set_role_permissions(role_id, permission_ids)

    return role_id

def set_role_permissions(role_id, permission_ids):
    """The function sets the permissions for a given role

    permissions_ids must be a list
    """
    # Clean user input
    role_id = str(role_id).strip()

    if not isinstance(permission_ids, list):
        raise ValidationError('Permission IDs passed incorrectly.')

    # Check if the role exists
    role = find_role(role_id, 'role_id')
    if role is None:
        raise ValidationError('The role does not exists.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Clear all permissions
    sql = """DELETE FROM role_permission WHERE role_id = %(role_id)s"""
    cursor.execute(sql, {'role_id': role_id})

    # Insert into role_permission
    sql = """INSERT INTO role_permission (
                role_id,
                permission_id
            ) VALUES (
                %(role_id)s,
                %(permission_id)s
            )"""
    for permission_id in permission_ids:
        cursor.execute(sql, {'role_id': role_id, 'permission_id': permission_id})
    dao.commit()

def add_permission(permission_name):
    # Clean user input
    permission_name = str(permission_name).strip()

    # Check if the permission exists
    if find_permission(permission_name, 'permission_name') is not None:
        raise ValidationError('The permission already exists.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Insert into role_permission
    sql = """INSERT INTO permission (
                permission_name
            ) VALUES (
                %(permission_name)s
            )"""
    cursor.execute(sql, {'permission_name': permission_name})
    dao.commit()

def find_permission(param, method):
    """The function will find the permission according to the method specified and the
    given parameter.

    Methods include 'permission_id' and 'permission_name'
    """
    # Check if the method is valid
    if method not in ['permission_id', 'permission_name']:
        raise ValidationError('Invalid method.')

    # Clean user input
    param = str(param).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query db for role
    sql = """SELECT * FROM permission WHERE """
    sql += method
    sql += """ = %(param)s"""
    cursor.execute(sql, {'param': param})
    result = cursor.fetchone()

    return result

def get_permissions(param, method):
    """Get the permission allowed
        Allowed methods includes 'user_id,' 'role_id' and 'role_name'
    """
    # Check if the method is valid
    if method not in ['user_id', 'role_id', 'role_name']:
        raise ValidationError('Invalid method.')

    # Clean user input
    param = str(param).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query db for role
    sql = ''
    if method == 'user_id':
        sql = """SELECT permission.permission_name FROM staff, role_permission,
                    permission WHERE
                    staff.user_id = %(param)s AND
                    staff.role_id = role_permission.role_id AND
                    role_permission.permission_id = permission.permission_id
                    ORDER BY permission.permission_name ASC"""
    elif method == 'role_id':
        sql = """SELECT permission.permission_name FROM role_permission,
                    permission WHERE
                    role_permission.role_id = %(param)s AND
                    role_permission.permission_id = permission.permission_id
                    ORDER BY permission.permission_name ASC"""
    else:
        sql = """SELECT permission.permission_name FROM role, role_permission,
                    permission WHERE
                    role.role_name = %(param)s AND
                    role.role_id = role_permission.role_id AND
                    role_permission.permission_id = permission.permission_id
                    ORDER BY permission.permission_name ASC"""
    cursor.execute(sql, {'param': param})
    result = cursor.fetchall()

    return result

def get_all_permissions():
    """The function will return all the permissions in the database"""
    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query db for role
    sql = """SELECT * FROM permission ORDER BY permission_name ASC"""
    cursor.execute(sql)
    result = cursor.fetchall()

    if result is None:
        return []

    return result

def delete_permission(permission_id):
    # Clean user input
    permission_id = str(permission_id).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Insert into role_permission
    sql = """DELETE FROM permission WHERE permission_id = %(permission_id)s"""
    cursor.execute(sql, {'permission_id': permission_id})
    dao.commit()
