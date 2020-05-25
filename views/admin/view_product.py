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
import controllers.controller_product as c
import controllers.controller_category as c_category
from utils.exception import ErrorMessage

admin_product = Blueprint('admin_product', __name__, template_folder='/templates')

@admin_product.route('/admin/product', methods=['GET'])
@staff_permission_required('products')
def product():
    category_id = request.args.get('category_id')
    if category_id is None or category_id == '0':
        products = c.get_all_products()
    else:
        products = c.get_products_by_category_id(category_id)
    return render_template('/admin/product.html',
        products = products,
        categories = c_category.list_categories(),
        category_id = category_id
    )

@admin_product.route('/admin/product/', methods=['GET'])
@staff_permission_required('products')
def product_empty():
    return redirect(url_for('.category'))

@admin_product.route('/admin/product/new', methods=['GET', 'POST'])
@staff_permission_required('products')
def new_product():
    if request.method == 'POST':
        res = c.add_product(
            product_name = request.values.get('productName'),
            description = request.values.get('productDescription'),
            priority = request.values.get('productPriority'),
            price = request.values.get('productPrice'),
            categories = request.form.getlist('categories')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('.product'))

@admin_product.route('/admin/product/update_image', methods=['GET', 'POST'])
@staff_permission_required('products')
def update_product_image():
    if request.method == 'POST':
        res = c.update_image(
            product_id = request.values.get('product_id'),
            update_type = request.values.get('update_type'),
            data = request.files['file'].read()
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('.product'))

@admin_product.route('/admin/product/edit', methods=['GET', 'POST'])
@staff_permission_required('products')
def edit_product():
    if request.method == 'POST':
        category = request.form.getlist('categories')
        res = edit_product(
            product_id = request.values.get('productID'),
            product_name = request.values.get('productName'),
            description = request.values.get('productDescription'),
            priority = request.values.get('productPriority'),
            price = request.values.get('productPrice'),
            categories = request.form.getlist('categories')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('.product'))

@admin_product.route('/admin/product/delete', methods=['GET', 'POST'])
@staff_permission_required('products')
def delete_product():
    id = request.values.get('product-id')
    res = c.remove_product(id)
    if isinstance(res, ErrorMessage):
        flash(res.get())
    return redirect(url_for('.product'))