from flask import Blueprint, render_template

staff_view = Blueprint('staff_view', __name__, template_folder='/templates')

@staff_view.route('/staff/dashboard', methods=['GET'])
def dashboard():
    return render_template('/staff/dashboard.html')

@staff_view.route('/staff/test/<string:template>', methods=['GET'])
def test_view(template):
    return render_template(template)

@staff_view.route('/base', methods=['GET'])
def base_view():
    return render_template('./shared/base.html')
