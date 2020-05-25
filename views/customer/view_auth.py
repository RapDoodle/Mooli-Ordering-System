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
import controllers.controller_product as c_product
import controllers.controller_category as c_category
import controllers.controller_user as c_user
import controllers.controller_authentication as c_auth
from utils.exception import ErrorMessage

auth_view = Blueprint('customer_auth', __name__, template_folder='/templates')

@auth_view.route('/login', methods=['GET'])
def login_redirect():
    return render_template('customer/login_redirect.html')

@auth_view.route('/login/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if request.values.get('password') != request.values.get('password_confirm'):
            # When the two passwords don't match
            # Error message here
            flash('Passwords do not match.')
            return render_template('customer/sign_up.html')
        user_id = c_user.sign_up(
            username = request.values.get('username'),
            email = request.values.get('email'), 
            password = request.values.get('password')
        )
        if isinstance(user_id, ErrorMessage):
            flash(user_id.get())
    return render_template('customer/sign_up.html')

@auth_view.route('/login/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        user_id = c_auth.login(
            username = request.values.get('username'),
            password = request.values.get('password')
        )
        if isinstance(user_id, ErrorMessage):
            flash(user_id.get())
            return redirect(url_for('.sign_in'))
        else:
            session['user_id'] = user_id
            return redirect(url_for('.home'))
    return render_template('customer/sign_in.html')