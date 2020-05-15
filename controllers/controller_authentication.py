from functools import wraps
from flask import session, flash, redirect, url_for
import models.model_user as m_user

def staff_permission(permission):
    return login_required

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Login is required.')
            return redirect(url_for('admin_view.login'))
        return fn(*args, **kwargs)
    return wrapper

def login(username, password):
    try:
        user_id = m_user.verify_credential(param = username, password = password, method = 'username')
    except Exception as e:
        return {'error': str(e)}
    return user_id
