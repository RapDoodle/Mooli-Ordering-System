import models.model_customer as model_customer
import models.model_redeem_card as model_redeem_card
import models.model_product as model_product

def find_customer(*args, **kwargs):
    return model_customer.find_customer(*args, **kwargs)

def get_redeem_cards(*args, **kwargs):
    return model_redeem_card.get_redeem_cards(*args, **kwargs)

def find_product(*args, **kwargs):
    return model_product.find_product(*args, **kwargs)
