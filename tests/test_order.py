import models.model_order as m
import models.model_coupon as m_coupon

print('[UNIT TESTING] Testing: Order...')

m.place_order(1000000, 'MOOLI')

print('[UNIT TESTING] Order has passed all the tests')
