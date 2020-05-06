from flask import Blueprint, render_template

staff_view = Blueprint('admin_view', __name__, template_folder='/templates')

@staff_view.route('/admin/dashboard', methods=['GET'])
def dashboard():
    return render_template('/admin/dashboard.html')

@staff_view.route('/admin/test/<string:template>', methods=['GET'])
def test_view(template):
    return render_template('/admin/' + template)
