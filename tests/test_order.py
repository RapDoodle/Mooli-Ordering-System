import models.model_order as m
import models.model_coupon as m_coupon

print(' * Testing: Order...')

m.place_order(user_id = 10000, coupon_code = 'MOOLI', payment = 'balance')

print(' ✓ Order has passed all the tests')
