from flask import Blueprint, render_template, request, redirect, url_for

import controllers.controller_category as c_category

admin_view = Blueprint('admin_view', __name__, template_folder='/templates')

@admin_view.route('/admin/dashboard', methods=['GET'])
def dashboard():
    return render_template('/admin/dashboard.html')

@admin_view.route('/admin/dashboard/category', methods=['GET'])
def category():
    return render_template('/admin/category.html', categories = c_category.list_categories())

@admin_view.route('/admin/dashboard/category/new', methods=['POST'])
def new_category():
    name = request.values.get('category-name')
    priority = request.values.get('category-priority')
    c_category.add_category(name, priority)
    return redirect(url_for('.category'), 200)

@admin_view.route('/admin/test/<string:template>', methods=['GET'])
def test_view(template):
    return render_template('/admin/' + template)
