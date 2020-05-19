from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages, session
from controllers.controller_authentication import staff_permission
import controllers.controller_category as c_category
import controllers.controller_product as c_product
import controllers.controller_authentication as c_auth
import controllers.controller_redeem_card as c_redeem_card
import controllers.controller_coupon as c_coupon
import controllers.controller_staff as c_staff
import controllers.controller_role as c_role

admin_view = Blueprint('admin_view', __name__, template_folder='/templates')

# ------------------- Login -------------------
@admin_view.route('/admin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = c_auth.staff_login(request.values.get('username'), request.values.get('password'))
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
    session.pop('is_staff', None)
    session.pop('username', None)
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

@admin_view.route('/admin/category/', methods=['GET'])
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
        msg = c_product.add_product(
                product_name = request.values.get('productName'),
                description = request.values.get('productDescription'),
                priority = request.values.get('productPriority'),
                price = request.values.get('productPrice'),
                categories = request.form.getlist('categories')
        )
        if 'error' in msg:
            flash(msg['error'])
    return redirect(url_for('.product'))

@admin_view.route('/admin/product/update_image', methods=['GET', 'POST'])
def update_product_image():
    if request.method == 'POST':
        msg = c_product.update_image(
            product_id = request.values.get('product_id'),
            update_type = request.values.get('update_type'),
            data = request.files['file'].read()
        )
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

# ------------------- Redeem Card -------------------
@admin_view.route('/admin/redeem_card', methods=['GET'])
def redeem_card():
    redeem_cards = c_redeem_card.get_redeem_cards()
    return render_template('/admin/redeem_card.html', redeem_cards = redeem_cards)

@admin_view.route('/admin/redeem_card/', methods=['GET'])
def redeem_card_empty():
    return redirect(url_for('.redeem_card'))

@admin_view.route('/admin/redeem_card/new', methods=['GET', 'POST'])
def new_redeem_cards():
    if request.method == 'POST':
        msg = c_redeem_card.add_redeem_cards(
                    value = request.values.get('value'),
                    batch = request.values.get('batch'))
        if 'error' in msg:
            flash(msg['error'])
    return redirect(url_for('.redeem_card'))

@admin_view.route('/admin/redeem_card/delete', methods=['GET', 'POST'])
def delete_redeem_card():
    msg = c_redeem_card.delete_redeem_card(redeem_code = request.values.get('redeem_code'))
    if 'error' in msg:
        flash(msg['error'])
    return redirect(url_for('.redeem_card'))

# ------------------- Coupon -------------------
@admin_view.route('/admin/coupon', methods=['GET'])
def coupon():
    return render_template('/admin/coupon.html',
            coupons = c_coupon.get_coupons()
    )

@admin_view.route('/admin/coupon/', methods=['GET'])
def coupon_empty():
    return redirect(url_for('.coupon'))

@admin_view.route('/admin/coupon/new', methods=['GET', 'POST'])
def new_coupon():
    if request.method == 'POST':
        msg = c_coupon.add_coupon(
                coupon_code = request.values.get('coupon_code'), 
                value = request.values.get('value'), 
                threshold = request.values.get('threshold'), 
                activate_date = request.values.get('activate_date'), 
                expire_date = request.values.get('expire_date')
        )
        if 'error' in msg:
            flash(msg['error'])
    return redirect(url_for('.coupon'))

@admin_view.route('/admin/coupon/edit', methods=['GET', 'POST'])
def edit_coupon():
    if request.method == 'POST':
        msg = c_coupon.update_coupon(
                coupon_code = request.values.get('coupon_code'), 
                value = request.values.get('value'), 
                threshold = request.values.get('threshold'), 
                activate_date = request.values.get('activate_date'), 
                expire_date = request.values.get('expire_date')
        )
        if 'error' in msg:
            flash(msg['error'])
    return redirect(url_for('.coupon'))

@admin_view.route('/admin/coupon/delete', methods=['GET', 'POST'])
def delete_coupon():
    msg = c_coupon.delete_coupon(coupon_code = request.values.get('coupon-code'))
    if 'error' in msg:
        flash(msg['error'])
    return redirect(url_for('.coupon'))

# ------------------- Staff -------------------
@admin_view.route('/admin/staff', methods=['GET'])
def staff():
    return render_template('/admin/staff.html',
            roles = c_role.get_all_roles(),
            staffs = c_staff.get_staff_list()
    )

@admin_view.route('/admin/staff/', methods=['GET'])
def staff_empty():
    return redirect(url_for('.staff'))

@admin_view.route('/admin/staff/new', methods=['GET', 'POST'])
def new_staff():
    if request.method == 'POST':
        msg = c_staff.add_staff(
                username = request.values.get('username'),
                email = request.values.get('email'), 
                password = request.values.get('password'), 
                role_id = request.values.get('role_id'), 
                first_name = request.values.get('first_name'),
                last_name = request.values.get('last_name'),
                gender = request.values.get('gender'),
                phone = request.values.get('phone')
        )
        if 'error' in msg:
            flash(msg['error'])
    return redirect(url_for('.staff'))

@admin_view.route('/admin/staff/edit', methods=['GET', 'POST'])
def edit_staff():
    if request.method == 'POST':
        msg = c_coupon.update_coupon(
                coupon_code = request.values.get('coupon_code'), 
                value = request.values.get('value'), 
                threshold = request.values.get('threshold'), 
                activate_date = request.values.get('activate_date'), 
                expire_date = request.values.get('expire_date')
        )
        if 'error' in msg:
            flash(msg['error'])
    return redirect(url_for('.staff'))

@admin_view.route('/admin/staff/delete', methods=['GET', 'POST'])
def delete_staff():
    msg = c_coupon.delete_coupon(coupon_code = request.values.get('coupon-code'))
    if 'error' in msg:
        flash(msg['error'])
    return redirect(url_for('.staff'))

# ------------------- Orders -------------------
@admin_view.route('/admin/order', methods=['GET'])
def order():
    return render_template('/admin/order.html',
            roles = c_role.get_all_roles(),
            staffs = c_staff.get_staff_list()
    )

@admin_view.route('/admin/order/', methods=['GET'])
def order_empty():
    return redirect(url_for('.order'))

@admin_view.route('/admin/order/edit', methods=['GET', 'POST'])
def edit_order():
    if request.method == 'POST':
        msg = c_coupon.update_coupon(
                coupon_code = request.values.get('coupon_code'), 
                value = request.values.get('value'), 
                threshold = request.values.get('threshold'), 
                activate_date = request.values.get('activate_date'), 
                expire_date = request.values.get('expire_date')
        )
        if 'error' in msg:
            flash(msg['error'])
    return redirect(url_for('.order'))

@admin_view.route('/admin/order/delete', methods=['GET', 'POST'])
def delete_order():
    msg = c_coupon.delete_coupon(coupon_code = request.values.get('coupon-code'))
    if 'error' in msg:
        flash(msg['error'])
    return redirect(url_for('.order'))

@admin_view.route('/admin/test/<string:template>', methods=['GET', 'GET'])
def test_view(template):
    return render_template('/admin/' + template)
