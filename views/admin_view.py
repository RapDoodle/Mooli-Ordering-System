from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages

import controllers.controller_category as c_category

admin_view = Blueprint('admin_view', __name__, template_folder='/templates')

@admin_view.route('/admin/dashboard', methods=['GET'])
def dashboard():
    return render_template('/admin/dashboard.html')

@admin_view.route('/admin/dashboard/category', methods=['GET'])
def category():
    return render_template('/admin/category.html', categories = c_category.list_categories(), messages = get_flashed_messages())

@admin_view.route('/admin/dashboard/category/', methods=['GET'])
def category_empty():
    return redirect(url_for('.category'))

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

@admin_view.route('/admin/test/<string:template>', methods=['GET', 'GET'])
def test_view(template):
    return render_template('/admin/' + template)
