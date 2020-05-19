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
    return render_template('customer/login_required.html', 
        product = product
    )

@customer_view.route('/test/<string:template>', methods=['GET'])
def test(template):
    return render_template('customer/' + template)
