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
import controllers.controller_category as c_category
import controllers.controller_product as c_product
import controllers.controller_authentication as c_auth
import controllers.controller_redeem_card as c_redeem_card
import controllers.controller_coupon as c_coupon
import controllers.controller_staff as c_staff
import controllers.controller_role as c_role
import controllers.controller_comment as c_comment
import controllers.controller_user as c_user
import controllers.controller_cart_item as c_cart_item
import controllers.controller_order as c_order

customer_view = Blueprint('customer_view', __name__, template_folder='/templates')

@customer_view.route('/', methods=['GET'])
def home():
    category_id = request.args.get('category_id')
    categories = c_category.list_categories()
    if category_id is None and len(categories) != 0:
        products = c_product.get_products_by_category_id(categories[0]['category_id'])
    else:
        products = c_product.get_products_by_category_id(category_id)
    return render_template('customer/home.html', 
        categories = categories,
        products = products
    )

@customer_view.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    product = c_product.get_product_by_product_id(product_id)
    if 'status' in product:
        return redirect(url_for('customer_view.home'))
    # When the product is found
    product['rating'] = c_comment.get_product_ratings(product_id)
    
    return render_template('customer/product.html', 
        product = product
    )

@customer_view.route('/login', methods=['GET'])
def login_redirect():
    return render_template('customer/login_redirect.html', 
        product = product
    )

@customer_view.route('/login/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if request.values.get('password') != request.values.get('password_confirm'):
            # When the two passwords don't match
            # Error message here
            flash('Passwords do not match.')
            return render_template('customer/sign_up.html')
        user_id = c_user.sign_up(
            username = request.values.get('username'),
            email = request.values.get('email'), 
            password = request.values.get('password')
        )
        if isinstance(user_id, dict):
            if 'error' in user_id:
                flash(user_id['error'])
                return redirect(url_for('.sign_up'))
        session['user_id'] = user_id
        return redirect(url_for('.home'))
    return render_template('customer/sign_up.html')

@customer_view.route('/login/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        user_id = c_auth.login(
            username = request.values.get('username'),
            password = request.values.get('password')
        )
        if isinstance(user_id, dict):
            if 'error' in user_id:
                flash(user_id['error'])
                return redirect(url_for('.sign_in'))
        else:
            session['user_id'] = user_id
            return redirect(url_for('.home'))
    return render_template('customer/sign_in.html')

@customer_view.route('/me', methods=['GET', 'POST'])
@c_auth.login_required
def me():
    user = c_user.find_user_by_id(session.get('user_id'))
    return render_template('customer/me.html', balance = user['balance'])

@customer_view.route('/me/redeem', methods=['GET', 'POST'])
@c_auth.login_required
def redeem():
    if request.method == 'POST':
        res = c_redeem_card.redeem(
            user_id = session.get('user_id'),
            redeem_code = request.values.get('redeem_code')
        )
        if isinstance(res, dict):
            if 'error' in res:
                flash(res['error'])
                return redirect(url_for('customer_view.redeem'))
        return redirect(url_for('customer_view.me'))
    return render_template('customer/redeem.html')

@customer_view.route('/me/account', methods=['GET', 'POST'])
@c_auth.login_required
def account():
    if request.method == 'POST':
        res = c_user.update_user_info(
            user_id = session.get('user_id'),
            first_name = request.values.get('first_name'),
            last_name = request.values.get('last_name'),
            gender = request.values.get('gender'),
            phone = request.values.get('phone')
        )
        if isinstance(res, dict):
            if 'error' in res:
                flash(res['error'])
                return redirect(url_for('customer_view.account'))
        return redirect(url_for('customer_view.me'))
    user = c_user.find_user_by_id(session.get('user_id'))
    return render_template('customer/account.html', user = user)

@customer_view.route('/me/logout', methods=['GET', 'POST'])
@c_auth.login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('customer_view.home'))

@customer_view.route('/cart', methods=['GET', 'POST'])
@c_auth.login_required
def cart():
    user_cart_items = c_cart_item.get_cart_items_by_user_id(session.get('user_id'))
    total = 0
    for user_cart_item in user_cart_items:
        total += user_cart_item['price'] * user_cart_item['amount']
    return render_template('customer/cart.html', 
        cart_items = user_cart_items,
        total = total
    )

@customer_view.route('/cart/add', methods=['GET', 'POST'])
@c_auth.login_required
def add_cart_item():
    if request.method == 'POST':
        res = c_cart_item.create_cart_item(
            user_id = session.get('user_id'),
            product_id = request.values.get('product_id'),
            amount = 1
        )
        if isinstance(res, dict):
            if 'error' in res:
                flash(res['error'])
                return redirect(url_for('customer_view.home'))
        return redirect(url_for('customer_view.cart'))
    return render_template('customer/cart.html')

@customer_view.route('/cart/update', methods=['GET', 'POST'])
@c_auth.login_required
def update_cart_items():
    if request.method == 'POST':
        user_cart_items = c_cart_item.get_cart_items_by_user_id(session.get('user_id'))
        for user_cart_item in user_cart_items:
            c_cart_item.update_cart_item_amount(
                cart_item_id = user_cart_item['cart_item_id'],
                amount = request.values.get('amount-for-' + str(user_cart_item['cart_item_id']))
            )
        return redirect(url_for('customer_view.cart'))
    return render_template('customer/cart.html')

@customer_view.route('/checkout/coupon', methods=['GET', 'POST'])
@c_auth.login_required
def checkout_coupon():
    if request.method == 'POST':
        res = coupon_code = c_coupon.check_coupon_validity(
            coupon_code = request.values.get('coupon_code'),
            user_id = session.get('user_id')
        )
        print(res)
        if isinstance(res, dict):
            if 'error' in res:
                flash(res['error'])
        elif isinstance(res, bool):
            print(res)
            if res == True:
                session['coupon_code'] = request.values.get('coupon_code')
                return redirect(url_for('customer_view.payment'))
            else:
                flash('You are not eligible for the coupon yet.')
    return render_template('customer/coupon.html')

@customer_view.route('/checkout/payment', methods=['GET', 'POST'])
@c_auth.login_required
def payment():
    total = c_cart_item.get_user_cart_total(session.get('user_id'))
    coupon = 0
    if session.get('coupon_code') is not None:
        coupon_info = c_coupon.find_coupon(session.get('coupon_code'))
        coupon = coupon_info['value']
    grand_total = total - coupon
    return render_template('customer/payment_method.html',
        total = total,
        coupon = coupon,
        grand_total = grand_total
    )

@customer_view.route('/checkout/confirm', methods=['POST'])
@c_auth.login_required
def place_order():
    res = c_order.place_order(session.get('user_id'), session.get('coupon_code'))
    if res is None:
        session.pop('coupon_code', None)
        return render_template('customer/order_placed.html')
    elif isinstance(res, dict):
        if 'error' in res:
            flash(res['error'])
    return redirect(url_for('customer_view.payment'))


@customer_view.route('/test/<string:template>', methods=['GET'])
def test(template):
    return render_template('customer/' + template)

