import models.model_user as m
from utils.exception import excpetion_handler

@excpetion_handler
def sign_up(*args, **kwargs):
        m.add_user(*args, **kwargs)

@excpetion_handler
def update_user_info(*args, **kwargs):
        m.update_user_info(*args, **kwargs)

@excpetion_handler
def change_password(user_id, old_password, new_password, verify_new_password):
    if not new_password == verify_new_password:
        return {'error': 'Passwords do not match.'}
    m.verify_credential(user_id, old_password, method = 'user_id')
    m.change_password(user_id, new_password)
