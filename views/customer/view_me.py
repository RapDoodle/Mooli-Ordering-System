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
import controllers.controller_cart_item as c_cart_item
import controllers.controller_user as c_user
import controllers.controller_redeem_card as c_redeem_card
from controllers.controller_authentication import login_required
from utils.exception import ErrorMessage

me_view = Blueprint('customer_me', __name__, template_folder='/templates')

@me_view.route('/me', methods=['GET', 'POST'])
@login_required
def me():
    user = c_user.find_user_by_id(session.get('user_id'))
    return render_template('customer/me.html', balance = user['balance'])

@me_view.route('/me/redeem', methods=['GET', 'POST'])
@login_required
def redeem():
    if request.method == 'POST':
        res = c_redeem_card.redeem(
            user_id = session.get('user_id'),
            redeem_code = request.values.get('redeem_code')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
            return redirect(url_for('customer_me.redeem'))
        return redirect(url_for('customer_me.me'))
    return render_template('customer/redeem.html')

@me_view.route('/me/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        res = c_user.update_user_info(
            user_id = session.get('user_id'),
            first_name = request.values.get('first_name'),
            last_name = request.values.get('last_name'),
            gender = request.values.get('gender'),
            phone = request.values.get('phone')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
            return redirect(url_for('customer_me.account'))
        return redirect(url_for('customer_me.me'))
    user = c_user.find_user_by_id(session.get('user_id'), decode_avatar=True)
    return render_template('customer/account.html', user = user)

@me_view.route('/me/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        res = c_user.change_password (
            user_id = session.get('user_id'),
            old_password = request.values.get('old_password'),
            new_password = request.values.get('new_password'),
            verify_new_password = request.values.get('new_password_confirm')
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
            return redirect(url_for('customer_me.change_password'))
        return redirect(url_for('customer_me.account'))
    user = c_user.find_user_by_id(session.get('user_id'))
    return render_template('customer/change_password.html', user = user)

@me_view.route('/me/change_avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    if request.method == 'POST':
        avatar = request.files['avatar'].read()
        res = c_user.update_user_avatar(
            user_id = session.get('user_id'),
            avatar = avatar
        )
        if isinstance(res, ErrorMessage):
            flash(res.get())
            return redirect(url_for('customer_me.change_avatar'))
    user = c_user.find_user_by_id(session.get('user_id'), decode_avatar = True)
    return render_template('customer/change_avatar.html', user = user)

@me_view.route('/me/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('customer_home.home'))