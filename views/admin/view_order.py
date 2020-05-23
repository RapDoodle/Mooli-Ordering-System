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
# from controllers.controller_staff import (
#     get_all_roles,
#     get_staff_list,
#     add_staff
# )
from utils.exception import ErrorMessage

admin_order = Blueprint('admin_order', __name__, template_folder='/templates')

@admin_order.route('/admin/order', methods=['GET'])
@staff_permission_required('orders')
def order():
    return render_template('/admin/order.html')

@admin_order.route('/admin/order/', methods=['GET'])
@staff_permission_required('orders')
def order_empty():
    return redirect(url_for('.order'))

@admin_order.route('/admin/order/edit', methods=['GET', 'POST'])
@staff_permission_required('orders')
def edit_order():
    # if request.method == 'POST':
    #     msg = c_coupon.update_coupon(
    #             coupon_code = request.values.get('coupon_code'), 
    #             value = request.values.get('value'), 
    #             threshold = request.values.get('threshold'), 
    #             activate_date = request.values.get('activate_date'), 
    #             expire_date = request.values.get('expire_date')
    #     )
    #     if 'error' in msg:
    #         flash(msg['error'])
    return redirect(url_for('.order'))

@admin_order.route('/admin/order/delete', methods=['GET', 'POST'])
@staff_permission_required('orders')
def delete_order():
    # msg = c_coupon.delete_coupon(coupon_code = request.values.get('coupon-code'))
    # if 'error' in msg:
    #     flash(msg['error'])
    return redirect(url_for('.order'))