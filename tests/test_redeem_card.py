import models.model_redeem_card as m

print('[UNIT TESTING] Testing: Redeem Card...')

m.add_redeem_cards(50, 50)
coupons = m.get_redeem_cards()
assert len(coupons) == 50
coupon_code_1 = coupons[0]['redeem_code']
assert m.find_redeem_card(coupon_code_1)['redeem_code'] == coupon_code_1
m.delete_redeem_card(coupon_code_1)
assert m.find_redeem_card(coupon_code_1) is None
assert len(m.get_redeem_cards(20, 10)) == 20
coupon_code_2 = coupons[1]['redeem_code']
m.redeem(1000000, coupon_code_2)

print('[UNIT TESTING] Redeem Card has passed all the tests')
