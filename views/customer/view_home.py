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
import controllers.controller_product as c_product
import controllers.controller_category as c_category
from utils.exception import ErrorMessage

home_view = Blueprint('customer_home', __name__, template_folder='/templates')

@home_view.route('/', methods=['GET'])
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

@home_view.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    product = c_product.get_product_by_product_id(product_id)
    if isinstance(product, ErrorMessage):
        flash(product.get())
        return redirect(url_for('customer_home.home'))
    return render_template('customer/product.html', 
        product = product
    )