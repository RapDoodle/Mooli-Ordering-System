from functools import wraps
from flask import session, flash, redirect, url_for
from utils.exception import excpetion_handler
from models.shared import find_staff
import models.model_user as m_user

def staff_permission(permission):
    def verify_staff_validity(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not session.get('user_id'):
                flash('Login is required.')
                return redirect(url_for('admin_view.login'))
            if not session.get('is_staff'):
                flash('You are not a staff.')
                return redirect(url_for('admin_view.login'))
            if not session.get('is_staff'):
                flash('You are not a staff.')
                return redirect(url_for('admin_view.login'))
            return fn(*args, **kwargs)
        return wrapper
    return verify_staff_validity

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Login is required.')
            return redirect(url_for('customer_view.login_redirect'))
        return fn(*args, **kwargs)
    return wrapper

@excpetion_handler
def login(username, password):
    user_id = m_user.verify_credential(param = username, password = password, method = 'username')
    return user_id

@excpetion_handler
def staff_login(username, password):
    # Find if the user is a staff
    staff = find_staff(param = username, method = 'username')

    if staff is None:
        return {'error': 'Not a staff.'}

    user_id = m_user.verify_credential(param = username, password = password, method = 'username')
    return staff
