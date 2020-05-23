import models.model_cart_item as m

print(' * Testing: Cart Item...')

m.create_cart_item(10000, 2, 2)
m.delete_cart_item(1)
m.create_cart_item(10000, 2, 3)
m.update_cart_item_amount(2, 2)
m.create_cart_item(10000, 3, 4)
m.create_cart_item(10001, 1, 8)
m.get_cart_items_by_user_id(10000)
assert list(m.get_cart_items_by_user_id(10000)[0].keys()) == ['cart_item_id', 'product_id', 'product_name', 'price', 'amount']

print(' ✓ Cart Item has passed all the tests')
