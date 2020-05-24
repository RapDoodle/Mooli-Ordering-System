import models.model_user as m
from utils.exception import excpetion_handler
from utils.exception import ErrorMessage

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
def find_user_by_id(user_id):
    return m.find_user(method = 'id', param = user_id)