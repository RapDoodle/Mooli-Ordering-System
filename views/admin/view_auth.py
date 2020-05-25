from flask import (
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash, 
    get_flashed_messages, 
    session
)
from controllers.controller_authentication import staff_permission_required, staff_login
from utils.exception import ErrorMessage

admin_auth = Blueprint('admin_auth', __name__, template_folder='/templates')

@admin_auth.route('/admin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = staff_login(request.values.get('username'), request.values.get('password'))
        if isinstance(res, dict) and len(res) == 3:
            session['user_id'] = res['user_id']
            session['is_staff'] = True
            session['username'] = res['username']
            return redirect(url_for('admin_dashboard.dashboard'))
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return render_template('/admin/login.html')

@admin_auth.route('/admin/', methods=['GET', 'POST'])
def login_empty():
    return redirect(url_for('admin_auth.login'))

@admin_auth.route('/admin/logout', methods=['GET'])
@staff_permission_required()
def logout():
    session.clear()
    return redirect(url_for('admin_auth.login'))