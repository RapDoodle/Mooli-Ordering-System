"""
This module serves as a gateway to other models while avoiding circular import
"""

def find_user(*args, **kwargs):
    import models.model_user as model_user
    return model_user.find_user(*args, **kwargs)

def get_redeem_cards(*args, **kwargs):
    import models.model_redeem_card as model_redeem_card
    return model_redeem_card.get_redeem_cards(*args, **kwargs)

def find_product(*args, **kwargs):
    import models.model_product as model_product
    return model_product.find_product(*args, **kwargs)

def get_items_by_user_id(*args, **kwargs):
    import models.model_item as model_item
    return model_item.get_items_by_user_id(*args, **kwargs)

def find_coupon(*args, **kwargs):
    import models.model_coupon as model_coupon
    return model_coupon.find_coupon(*args, **kwargs)

def find_coupon_and_check_validity(*args, **kwargs):
    import models.model_coupon as model_coupon
    return model_coupon.find_coupon_and_check_validity(*args, **kwargs)
