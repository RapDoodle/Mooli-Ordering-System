from flask import Blueprint, render_template

customer_home_view = Blueprint('customer_home_routes', __name__)

@customer_home_view.route('/', methods=['GET'])
def home():
    return ('<h1>Hello World</h1>')
