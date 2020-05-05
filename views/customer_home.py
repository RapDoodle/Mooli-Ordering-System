from flask import Blueprint, render_template

customer_home_view = Blueprint('customer_home_routes', __name__, template_folder='/templates')

@customer_home_view.route('/', methods=['GET'])
def home():
    return render_template('customer/home.html')

@customer_home_view.route('/test/<string:template>', methods=['GET'])
def test(template):
    return render_template('customer/' + template)
