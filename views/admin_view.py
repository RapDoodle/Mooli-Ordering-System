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
        result = c_auth.staff_login(request.values.get('username'), request.values.get('password'))
        print(result)
        if isinstance(result, dict) and len(result) == 3:
            session['user_id'] = result['user_id']
            session['is_staff'] = True
            session['username'] = result['username']
            return redirect(url_for('admin_view.dashboard'))
        if isinstance(result, dict) and len(result) == 1:
            # Most likely that an exception has been thrown
            if 'error' in result:
                flash(result['error'])
    return render_template('/admin/login.html')

@admin_view.route('/admin/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('admin_view.login'))

# ------------------- Dashboard -------------------

@admin_view.route('/admin/dashboard', methods=['GET'])
@staff_permission('T')
def dashboard():
    return render_template('/admin/dashboard.html')

# ------------------- Category -------------------
@admin_view.route('/admin/category', methods=['GET'])
def category():
    categories = c_category.list_categories()
    return render_template('/admin/category.html', categories = categories)

@admin_view.route('/admin/dashboard/category/', methods=['GET'])
def category_empty():
    return redirect(url_for('.category'))

#
@admin_view.route('/admin/category/new', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':
        name = request.values.get('category-name')
        priority = request.values.get('category-priority')
        msg = c_category.add_category(name, priority)
        if 'error' in msg:
            print(msg['error'])
            flash(msg['error'])
    return redirect(url_for('.category'))

@admin_view.route('/admin/category/edit', methods=['GET', 'POST'])
def edit_category():
    id = request.values.get('category-id')
    name = request.values.get('category-name')
    priority = request.values.get('category-priority')
    msg = c_category.update_category(id, name, priority)
    if 'error' in msg:
        flash(msg['error'])
    return redirect(url_for('.category'))

@admin_view.route('/admin/category/delete', methods=['GET', 'POST'])
def delete_category():
    id = request.values.get('category-id')
    msg = c_category.remove_category(id)
    if 'error' in msg:
        flash(msg['error'])
    return redirect(url_for('.category'))

# ------------------- Product -------------------
@admin_view.route('/admin/product', methods=['GET'])
def product():
    category_id = request.args.get('category_id')
    if category_id is None or category_id == '0':
        products = c_product.get_all_products()
    else:
        products = c_product.get_products_by_category_id(category_id)
    return render_template('/admin/product.html',
            products = products,
            categories = c_category.list_categories(),
            category_id = category_id
    )

@admin_view.route('/admin/product/', methods=['GET'])
def product_empty():
    return redirect(url_for('.category'))

@admin_view.route('/admin/product/new', methods=['GET', 'POST'])
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

@admin_view.route('/admin/product/edit', methods=['GET', 'POST'])
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

@admin_view.route('/admin/product/delete', methods=['GET', 'POST'])
def delete_product():
    id = request.values.get('product-id')
    msg = c_product.remove_product(id)
    if 'error' in msg:
        flash(msg['error'])
    return redirect(url_for('.product'))

@admin_view.route('/admin/test/<string:template>', methods=['GET', 'GET'])
def test_view(template):
    return render_template('/admin/' + template)
