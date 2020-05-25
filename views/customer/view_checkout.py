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
import controllers.controller_coupon as c_coupon
import controllers.controller_cart_item as c_cart_item
import controllers.controller_order as c_order
from controllers.controller_authentication import login_required
from utils.exception import ErrorMessage

checkout_view = Blueprint('customer_checkout', __name__, template_folder='/templates')

@checkout_view.route('/checkout/coupon', methods=['GET', 'POST'])
@login_required
def checkout_coupon():
    if request.method == 'POST':
        res = coupon_code = c_coupon.check_coupon_validity(
            coupon_code = request.values.get('coupon_code'),
            user_id = session.get('user_id')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
        elif isinstance(res, bool):
            if res == True:
                session['coupon_code'] = request.values.get('coupon_code')
                return redirect(url_for('.payment'))
            else:
                flash('You are not eligible for the coupon yet.')
    return render_template('customer/coupon.html', coupon_code = str(session.get('coupon_code')))

@checkout_view.route('/checkout/payment', methods=['GET', 'POST'])
@login_required
def payment():
    total = c_cart_item.get_user_cart_total(session.get('user_id'))
    discount = 0
    if session.get('coupon_code') is not None:
        coupon_info = c_coupon.find_coupon(session.get('coupon_code'))
        discount = coupon_info['value']
    grand_total = total - discount
    return render_template('customer/payment_method.html',
        total = total,
        discount = discount,
        grand_total = grand_total
    )

@checkout_view.route('/checkout/confirm', methods=['POST'])
@login_required
def place_order():
    res = c_order.place_order(session.get('user_id'), session.get('coupon_code'))
    if res is None:
        session.pop('coupon_code', None)
        return render_template('customer/order_placed.html')
    elif isinstance(res, ErrorMessage):
        flash(res.get())
    return redirect(url_for('.payment'))

