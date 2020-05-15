from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages, session
from controllers.controller_authentication import staff_permission
import controllers.controller_category as c_category
import controllers.controller_product as c_product
import controllers.controller_authentication as c_auth

admin_view = Blueprint('admin_view', __name__, template_folder='/templates')

# ------------------- Login -------------------
@admin_view.route('/admin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = c_auth.login(request.values.get('username'), request.values.get('password'))
        if isinstance(result, int):
            session['user_id'] = result
            return redirect(url_for('admin_view.dashboard'))
        if isinstance(result, dict):
            # Most likely that an exception has been thrown
            if 'error' in result:
                flash(result['error'])
    return render_template('/admin/login.html')

@admin_view.route('/admin/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('admin_view.login'))

@admin_view.route('/admin/dashboard', methods=['GET'])
@staff_permission('T')
def dashboard():
    return render_template('/admin/dashboard.html')

# ------------------- Category -------------------
@admin_view.route('/admin/dashboard/category', methods=['GET'])
def category():
    session['h'] = 5
    categories = c_category.list_categories()
    return render_template('/admin/category.html', categories = categories, messages = get_flashed_messages())

@admin_view.route('/admin/dashboard/category/', methods=['GET'])
def category_empty():
    return redirect(url_for('.category'))

#
@admin_view.route('/admin/dashboard/category/new', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':
        name = request.values.get('category-name')
        priority = request.values.get('category-priority')
        msg = c_category.add_category(name, priority)
        if 'error' in msg:
            flash(msg['error'])
    return redirect(url_for('.category'))

@admin_view.route('/admin/dashboard/category/edit', methods=['GET', 'POST'])
def edit_category():
    id = request.values.get('category-id')
    name = request.values.get('category-name')
    priority = request.values.get('category-priority')
    msg = c_category.update_category(id, name, priority)
    if 'error' in msg:
        flash(msg['error'])
    return redirect(url_for('.category'))

@admin_view.route('/admin/dashboard/category/delete', methods=['GET', 'POST'])
def delete_category():
    id = request.values.get('category-id')
    msg = c_category.remove_category(id)
    if 'error' in msg:
        flash(msg['error'])
    return redirect(url_for('.category'))

# ------------------- Product -------------------
@admin_view.route('/admin/dashboard/product', methods=['GET'])
def product():
    print(session['h'])
    return render_template('/admin/product.html',
            products = c_product.get_all_products(),
            categories = c_category.list_categories(),
            messages = get_flashed_messages()
    )

@admin_view.route('/admin/dashboard/product/', methods=['GET'])
def product_empty():
    return redirect(url_for('.category'))

#
@admin_view.route('/admin/dashboard/product/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        category = request.form.getlist('categories')
        print(request.values.get('productName'),request.values.get('productDescription'),request.values.get('productPriority'),request.values.get('productPrice'),request.form.getlist('categories'))
        msg = c_product.add_product(
                product_name = request.values.get('productName'),
                description = request.values.get('productDescription'),
                priority = request.values.get('productPriority'),
                price = request.values.get('productPrice'),
                categories = request.form.getlist('categories')
        )
        print(msg)
        if 'error' in msg:
            flash(msg['error'])
    return redirect(url_for('.product'))

@admin_view.route('/admin/dashboard/product/edit', methods=['GET', 'POST'])
def edit_product():
    if request.method == 'POST':
        category = request.form.getlist('categories')
        print(request.values.get('productName'),request.values.get('productDescription'),request.values.get('productPriority'),request.values.get('productPrice'),request.form.getlist('categories'))
        msg = c_product.edit_product(
                product_id = request.values.get('productID'),
                product_name = request.values.get('productName'),
                description = request.values.get('productDescription'),
                priority = request.values.get('productPriority'),
                price = request.values.get('productPrice'),
                categories = request.form.getlist('categories')
        )
        print(msg)
        if 'error' in msg:
            flash(msg['error'])
    return redirect(url_for('.product'))

@admin_view.route('/admin/dashboard/product/delete', methods=['GET', 'POST'])
def delete_product():
    id = request.values.get('product-id')
    msg = c_product.remove_product(id)
    if 'error' in msg:
        flash(msg['error'])
    return redirect(url_for('.product'))


@admin_view.route('/admin/test/<string:template>', methods=['GET', 'GET'])
def test_view(template):
    return render_template('/admin/' + template)
