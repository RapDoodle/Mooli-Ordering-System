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

admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='/templates')

@admin_dashboard.route('/admin/dashboard', methods=['GET'])
@staff_permission_required()
def dashboard():
    return render_template('/admin/dashboard.html')
    