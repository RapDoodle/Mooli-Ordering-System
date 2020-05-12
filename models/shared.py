import models.model_customer as model_customer
import models.model_redeem_card as model_redeem_card

def find_customer(*args, **kwargs):
    return model_customer.find_customer(*args, **kwargs)

def get_redeem_cards(*args, **kwargs):
    return model_redeem_card.get_redeem_cards(*args, **kwargs)
