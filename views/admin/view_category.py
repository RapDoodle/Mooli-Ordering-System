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
from utils.exception import ErrorMessage
import controllers.controller_category as c

admin_category = Blueprint('admin_category', __name__, template_folder='/templates')

@admin_category.route('/admin/category', methods=['GET'])
@staff_permission_required('categories')
def category():
    categories = c.list_categories()
    return render_template('/admin/category.html', categories = categories)

@admin_category.route('/admin/category/', methods=['GET'])
@staff_permission_required('categories')
def category_empty():
    return redirect(url_for('.category'))

@admin_category.route('/admin/category/new', methods=['GET', 'POST'])
@staff_permission_required('categories')
def new_category():
    if request.method == 'POST':
        name = request.values.get('category-name')
        priority = request.values.get('category-priority')
        res = c.add_category(name, priority)
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('.category'))

@admin_category.route('/admin/category/edit', methods=['GET', 'POST'])
@staff_permission_required('categories')
def edit_category():
    id = request.values.get('category-id')
    name = request.values.get('category-name')
    priority = request.values.get('category-priority')
    res = c.update_category(id, name, priority)
    if isinstance(res, ErrorMessage):
        flash(res.get())
    return redirect(url_for('.category'))

@admin_category.route('/admin/category/delete', methods=['GET', 'POST'])
@staff_permission_required('categories')
def delete_category():
    id = request.values.get('category-id')
    res = c.remove_category(id)
    if isinstance(res, ErrorMessage):
        flash(res.get())
    return redirect(url_for('.category'))