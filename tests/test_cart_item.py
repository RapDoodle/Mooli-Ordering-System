import models.model_cart_item as m

print(' * Testing: Cart Item...')

m.create_cart_item(10000, 2, 2)
m.delete_cart_item(1)
m.create_cart_item(10000, 2, 3)
m.update_cart_item_amount(2, 2)
m.create_cart_item(10000, 3, 4)
m.create_cart_item(10001, 1, 8)
assert len(m.get_cart_items_by_user_id(10000)) == 2

print(' ✓ Cart Item has passed all the tests')
