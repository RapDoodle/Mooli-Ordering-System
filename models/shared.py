"""
This module serves as a gateway to other models while avoiding circular import
"""

def find_user(*args, **kwargs):
    from models.model_user import find_user
    return find_user(*args, **kwargs)

def add_user(*args, **kwargs):
    from models.model_user import add_user
    return add_user(*args, **kwargs)

def get_redeem_cards(*args, **kwargs):
    from models.model_redeem_card import get_redeem_cards
    return get_redeem_cards(*args, **kwargs)

def find_product(*args, **kwargs):
    from models.model_product import find_product
    return find_product(*args, **kwargs)

def get_items_by_user_id(*args, **kwargs):
    from models.model_item import get_items_by_user_id
    return get_items_by_user_id(*args, **kwargs)

def find_coupon(*args, **kwargs):
    from models.model_coupon import find_coupon
    return find_coupon(*args, **kwargs)

def find_coupon_and_check_validity(*args, **kwargs):
    from models.model_coupon import find_coupon_and_check_validity
    return find_coupon_and_check_validity(*args, **kwargs)

def get_items_by_user_id(*args, **kwargs):
    from models.model_item import get_items_by_user_id
    return get_items_by_user_id(*args, **kwargs)

def get_archive_index(*args, **kwargs):
    from models.model_archive import get_archive_index
    return get_archive_index(*args, **kwargs)
