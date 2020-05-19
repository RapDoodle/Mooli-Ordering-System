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
from controllers.controller_authentication import staff_permission
import controllers.controller_category as c_category
import controllers.controller_product as c_product
import controllers.controller_authentication as c_auth
import controllers.controller_redeem_card as c_redeem_card
import controllers.controller_coupon as c_coupon
import controllers.controller_staff as c_staff
import controllers.controller_role as c_role
import controllers.controller_comment as c_comment
import controllers.controller_user as c_user

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
    return render_template('customer/redeem.html')

@customer_view.route('/me/account', methods=['GET', 'POST'])
@c_auth.login_required
def account():
    return render_template('customer/redeem.html')

@customer_view.route('/me/logout', methods=['GET', 'POST'])
@c_auth.login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('customer_view.home'))

@customer_view.route('/cart', methods=['GET', 'POST'])
@c_auth.login_required
def cart():
    return render_template('customer/cart.html')

@customer_view.route('/test/<string:template>', methods=['GET'])
def test(template):
    return render_template('customer/' + template)
