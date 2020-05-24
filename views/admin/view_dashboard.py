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
from controllers.controller_authentication import staff_permission_required
import controllers.controller_user as c_user
from utils.exception import ErrorMessage
admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='/templates')

@admin_dashboard.route('/admin/dashboard', methods=['GET'])
@staff_permission_required()
def dashboard():
    return render_template('/admin/dashboard.html')
    
@admin_dashboard.route('/admin/dashboard/change_password', methods=['GET', 'POST'])
@staff_permission_required()
def change_password():
    if request.method == 'POST':
        res = c_user.change_password (
            user_id = session.get('user_id'),
            old_password = request.values.get('old_password'),
            new_password = request.values.get('new_password'),
            verify_new_password = request.values.get('new_password_confirm')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('admin_dashboard.dashboard'))
    