import models.model_user as m

def sign_up(*args, **kwargs):
    try:
        m.add_user(*args, **kwargs)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'You account has been created successfully.'}

def update_user_info(*args, **kwargs):
    try:
        m.update_user_info(*args, **kwargs)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'You account info has been updated successfully.'}

def change_password(user_id, old_password, new_password, verify_new_password):
    if not new_password == verify_new_password:
        return {'error': 'Passwords do not match.'}
    try:
        m.verify_credential(user_id, old_password, method = 'user_id')
        m.change_password(user_id, new_password)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'You password has been updated successfully.'}
