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
from utils.exception import ErrorMessage
import controllers.controller_coupon as c

admin_coupon = Blueprint('admin_coupon', __name__, template_folder='/templates')

@admin_coupon.route('/admin/coupon', methods=['GET'])
@staff_permission_required('coupons')
def coupon():
    return render_template('/admin/coupon.html',
        coupons = c.get_coupons()
    )

@admin_coupon.route('/admin/coupon/', methods=['GET'])
def coupon_empty():
    return redirect(url_for('.coupon'))

@admin_coupon.route('/admin/coupon/new', methods=['GET', 'POST'])
@staff_permission_required('coupons')
def new_coupon():
    if request.method == 'POST':
        res = c.add_coupon(
            coupon_code = request.values.get('coupon_code'), 
            value = request.values.get('value'), 
            threshold = request.values.get('threshold'), 
            activate_date = request.values.get('activate_date'), 
            expire_date = request.values.get('expire_date')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('.coupon'))

@admin_coupon.route('/admin/coupon/edit', methods=['GET', 'POST'])
@staff_permission_required('coupons')
def edit_coupon():
    if request.method == 'POST':
        res = c.update_coupon(
            coupon_code = request.values.get('coupon_code'), 
            value = request.values.get('value'), 
            threshold = request.values.get('threshold'), 
            activate_date = request.values.get('activate_date'), 
            expire_date = request.values.get('expire_date')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('.coupon'))

@admin_coupon.route('/admin/coupon/delete', methods=['GET', 'POST'])
@staff_permission_required('coupons')
def delete_coupon():
    res = c.delete_coupon(coupon_code = request.values.get('coupon_code'))
    if isinstance(res, ErrorMessage):
        flash(res.get())
    return redirect(url_for('.coupon'))