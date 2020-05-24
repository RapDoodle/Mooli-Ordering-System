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
from utils.pagination import get_page_numbers
import controllers.controller_redeem_card as c

admin_redeem_card = Blueprint('admin_redeem_card', __name__, template_folder='/templates')

@admin_redeem_card.route('/admin/redeem_card', methods=['GET'])
@staff_permission_required('redeem_cards')
def redeem_card():
    page = request.args.get('page')
    if page is None:
        page = 1
    redeem_cards = c.get_redeem_cards(page)
    pages = get_page_numbers(c.count_records_length(), page)
    return render_template('/admin/redeem_card.html', 
        redeem_cards = redeem_cards, 
        pages = pages, 
        current_page = str(page)
    )

@admin_redeem_card.route('/admin/redeem_card/', methods=['GET'])
@staff_permission_required('redeem_cards')
def redeem_card_empty():
    return redirect(url_for('.redeem_card'))

@admin_redeem_card.route('/admin/redeem_card/new', methods=['GET', 'POST'])
@staff_permission_required('redeem_cards')
def new_redeem_cards():
    if request.method == 'POST':
        res = c.add_redeem_cards(
            value = request.values.get('value'),
            batch = request.values.get('batch'))
        if isinstance(res, ErrorMessage):
            flash(res.get())
    return redirect(url_for('.redeem_card'))

@admin_redeem_card.route('/admin/redeem_card/delete', methods=['GET', 'POST'])
@staff_permission_required('redeem_cards')
def delete_redeem_card():
    res = c.delete_redeem_card(redeem_code = request.values.get('redeem_code'))
    if isinstance(res, ErrorMessage):
        flash(res.get())
    return redirect(url_for('.redeem_card'))