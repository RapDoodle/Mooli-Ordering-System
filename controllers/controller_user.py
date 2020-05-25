import models.model_user as m
from utils.exception import excpetion_handler
from utils.exception import ErrorMessage
import base64

@excpetion_handler
def sign_up(*args, **kwargs):
    return m.add_user(*args, **kwargs)

@excpetion_handler
def update_user_info(*args, **kwargs):
    return m.update_user_info(*args, **kwargs)

@excpetion_handler
def change_password(user_id, old_password, new_password, verify_new_password):
    if not new_password == verify_new_password:
        return ErrorMessage('New passwords do not match.')
    m.verify_credential(user_id, old_password, method = 'user_id')
    m.change_password(user_id, new_password)

@excpetion_handler
def find_user_by_id(user_id, decode_avatar = False):
    # Fix for outputing the gender in binary
    user = m.find_user(method = 'id', param = user_id)
    if user is not None:
        user['gender'] = user['gender'].decode('utf-8')
    if decode_avatar and user is not None:
        if 'avatar' in user and user['avatar'] is not None:
            e = base64.b64encode(user['avatar'])
            user['avatar'] = e.decode("UTF-8")
        else:
            user['avatar'] = 'None'
    return user

@excpetion_handler
def update_user_avatar(*args, **kwargs):
    return m.update_user_avatar(*args, **kwargs)

    