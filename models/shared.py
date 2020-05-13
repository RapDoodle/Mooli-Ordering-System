import models.model_user as model_user
import models.model_redeem_card as model_redeem_card
import models.model_product as model_product

def find_user(*args, **kwargs):
    return model_user.find_user(*args, **kwargs)

def get_redeem_cards(*args, **kwargs):
    return model_redeem_card.get_redeem_cards(*args, **kwargs)

def find_product(*args, **kwargs):
    return model_product.find_product(*args, **kwargs)
