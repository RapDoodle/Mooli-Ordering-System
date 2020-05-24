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
import controllers.controller_order as c
from utils.exception import ErrorMessage
from utils.interpreter import interprete_order_status

admin_order = Blueprint('admin_order', __name__, template_folder='/templates')

@admin_order.route('/admin/order', methods=['GET'])
@staff_permission_required('orders')
def order():
    scope_id = request.args.get('scope_id')
    scope_id = str(scope_id).strip()
    print(scope_id)
    if scope_id == '0' or scope_id == 'None':
        # On going orders
        orders = c.get_on_going_orders()
        if isinstance(orders, ErrorMessage):
            flash(orders.get())
            return render_template('/admin/order_on_going.html')
        return render_template('/admin/order_on_going.html',
            orders = orders,
            interpreter = interprete_order_status,
            orders_len = len(orders)
        )
    else:
        # All orders
        orders = c.get_all_orders()
        if isinstance(orders, ErrorMessage):
            flash(orders.get())
        return render_template('/admin/order_all.html',
            orders = orders,
            interpreter = interprete_order_status
        )

@admin_order.route('/admin/order/', methods=['GET'])
@staff_permission_required('orders')
def order_empty():
    return redirect(url_for('.order'))

@admin_order.route('/admin/order/update', methods=['GET', 'POST'])
@staff_permission_required('orders')
def update_status():
    if request.method == 'POST':
        res = c.update_order_status(
            order_id = request.values.get('order_id'),
            status = request.values.get('status')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('.order'))

@admin_order.route('/admin/order/refund', methods=['GET', 'POST'])
@staff_permission_required('orders')
def refund():
    if request.method == 'POST':
        res = c.order_refund(
            order_id = request.values.get('order_id')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('.order'))

@admin_order.route('/admin/order/details/<int:order_id>', methods=['GET'])
@staff_permission_required('orders')
def details(order_id):
    order = c.get_order(order_id = order_id)
    return render_template('/admin/order_details.html',
        order = order,
        interpreter = interprete_order_status
    )