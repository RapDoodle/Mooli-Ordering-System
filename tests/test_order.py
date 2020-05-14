import models.model_order as m
import models.model_coupon as m_coupon

print(' * Testing: Order...')

m.place_order(10000, 'MOOLI')

print(' ✓ Order has passed all the tests')
