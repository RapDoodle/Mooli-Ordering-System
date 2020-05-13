import models.model_coupon as m

print('[UNIT TESTING] Testing: Coupon...')

m.add_coupon('SUMMERSALE', 5, 20, '2020-5-1', '2020-9-1')
m.add_coupon('THANKYOU2020', 20, 50, '2020-1-1', '2020-12-31')
assert len(m.get_coupons()) == 2
m.delete_coupon('THANKYOU2020')
assert len(m.get_coupons()) == 1
m.add_coupon('THANKSGIVING', 50, 100, '2020-11-5', '2020-11-6')
m.add_coupon('LOVEYOU2019', 50, 100, '2019-12-1', '2019-12-31')
m.add_coupon('MOOLI', 20, 100)

print('[UNIT TESTING] Coupon has passed all the tests')
