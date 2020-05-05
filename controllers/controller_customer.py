import models.model_customer as m

def sign_up(username, email, password, first_name = '', last_name = '', gender = '', phone = ''):
    try:
        m.add_customer(username, email, password, first_name, last_name, gender, phone)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'You account has been created successfully.'}

def update_customer_info(customer_id, first_name = '', last_name = '', gender = '', phone = ''):
    try:
        m.update_customer_info(customer_id, first_name, last_name, gender, phone)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'You account info has been updated successfully.'}

def change_password(customer_id, old_password, new_password, verify_new_password):
    if not new_password == verify_new_password:
        return {'error': 'Passwords do not match.'}
    try:
        m.verify_credential(customer_id, old_password, method = 'customer_id')
        m.change_password(customer_id, new_password)
    except Exception as e:
        return {'error': str(e)}
    return {'message': 'You password has been updated successfully.'}
