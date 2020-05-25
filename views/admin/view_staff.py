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
import controllers.controller_staff as c
import controllers.controller_role as c_role
from utils.exception import ErrorMessage

admin_staff = Blueprint('admin_staff', __name__, template_folder='/templates')

@admin_staff.route('/admin/staff', methods=['GET'])
@staff_permission_required('staff')
def staff():
    return render_template('/admin/staff.html',
        roles = c_role.get_all_roles(),
        staffs = c.get_staff_list()
    )

@admin_staff.route('/admin/staff/', methods=['GET'])
@staff_permission_required('staff')
def staff_empty():
    return redirect(url_for('.staff'))

@admin_staff.route('/admin/staff/new', methods=['GET', 'POST'])
@staff_permission_required('staff')
def new_staff():
    if request.method == 'POST':
        res = c.add_staff(
            username = request.values.get('username'),
            email = request.values.get('email'), 
            password = request.values.get('password'), 
            role_id = request.values.get('role_id'), 
            first_name = request.values.get('first_name'),
            last_name = request.values.get('last_name'),
            gender = request.values.get('gender'),
            phone = request.values.get('phone')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('.staff'))

@admin_staff.route('/admin/staff/edit', methods=['GET', 'POST'])
@staff_permission_required('staff')
def edit_staff():
    if request.method == 'POST':
        res = c.update_staff(
            user_id = session.get('user_id'),
            role_id = request.values.get('role_id'),
            first_name = request.values.get('first_name'),
            last_name = request.values.get('last_name'),
            gender = request.values.get('gender'),
            phone = request.values.get('phone')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('.staff'))

@admin_staff.route('/admin/staff/delete', methods=['GET', 'POST'])
@staff_permission_required('staff')
def delete_staff():
    res = c.delete_staff(user_id = request.values.get('user_id'))
    if isinstance(res, ErrorMessage):
        flash(res.get())
    return redirect(url_for('.staff'))