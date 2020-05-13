import models.model_coupon as m

print('[UNIT TESTING] Testing: Coupon...')

m.add_coupon('SUMMERSALE', 5, 20)
m.add_coupon('THANKYOU2020', 10, 20, '2020-1-1', '2020-12-31')
assert len(m.get_coupons()) == 2
m.delete_coupon('THANKYOU2020')
assert len(m.get_coupons()) == 1

print('[UNIT TESTING] Coupon has passed all the tests')
