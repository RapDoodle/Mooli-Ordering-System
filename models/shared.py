"""
This module serves as a gateway to other models while avoiding circular import
"""

def find_user(*args, **kwargs):
    from models.model_user import find_user
    return find_user(*args, **kwargs)

def user_pay(*args, **kwargs):
    from models.model_user import user_pay
    return user_pay(*args, **kwargs)

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

def get_cart_items_by_user_id(*args, **kwargs):
    from models.model_cart_item import get_cart_items_by_user_id
    return get_cart_items_by_user_id(*args, **kwargs)

def create_purchased_item(*args, **kwargs):
    from models.model_purchased_item import create_purchased_item
    return create_purchased_item(*args, **kwargs)

def get_archive_index(*args, **kwargs):
    from models.model_archive import get_archive_index
    return get_archive_index(*args, **kwargs)

def find_role(*args, **kwargs):
    from models.model_role import find_role
    return find_role(*args, **kwargs)

def find_staff(*args, **kwargs):
    from models.model_staff import find_staff
    return find_staff(*args, **kwargs)

def get_product_ratings(*args, **kwargs):
    from models.model_comment import get_product_ratings
    return get_product_ratings(*args, **kwargs)

def delete_cart_item(*args, **kwargs):
    from models.model_cart_item import delete_cart_item
    return delete_cart_item(*args, **kwargs)