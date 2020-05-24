import models.model_redeem_card as m
from utils.exception import excpetion_handler

@excpetion_handler
def add_redeem_cards(*args, **kwargs):
    return m.add_redeem_cards(*args, **kwargs)

@excpetion_handler
def get_redeem_cards(page = 1):
    # Each page contains 20 records
    try:
        page = int(page)
    except:
        page = 1
    return m.get_redeem_cards(limit = 20, offset = (page - 1) * 20)

@excpetion_handler
def delete_redeem_card(*args, **kwargs):
    return m.delete_redeem_card(*args, **kwargs)

@excpetion_handler
def redeem(*args, **kwargs):
    return m.redeem(*args, **kwargs)

@excpetion_handler
def count_records_length():
    return m.count_records_length()