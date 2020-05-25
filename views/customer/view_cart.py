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
import controllers.controller_cart_item as c_cart_item
from controllers.controller_authentication import login_required
from utils.exception import ErrorMessage

cart_view = Blueprint('customer_cart', __name__, template_folder='/templates')

@cart_view.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    user_cart_items = c_cart_item.get_cart_items_by_user_id(session.get('user_id'))
    total = 0
    for user_cart_item in user_cart_items:
        total += user_cart_item['price'] * user_cart_item['amount']
    return render_template('customer/cart.html', 
        cart_items = user_cart_items,
        total = total
    )

@cart_view.route('/cart/add', methods=['GET', 'POST'])
@login_required
def add_cart_item():
    if request.method == 'POST':
        res = c_cart_item.create_cart_item(
            user_id = session.get('user_id'),
            product_id = request.values.get('product_id'),
            amount = 1
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
            return redirect(url_for('.home'))
    return redirect(url_for('.cart'))

@cart_view.route('/cart/update', methods=['GET', 'POST'])
@login_required
def update_cart_items():
    if request.method == 'POST':
        user_cart_items = c_cart_item.get_cart_items_by_user_id(session.get('user_id'))
        for user_cart_item in user_cart_items:
            c_cart_item.update_cart_item_amount(
                cart_item_id = user_cart_item['cart_item_id'],
                amount = request.values.get('amount-for-' + str(user_cart_item['cart_item_id']))
            )
        return redirect(url_for('.cart'))
    return render_template('customer/cart.html')