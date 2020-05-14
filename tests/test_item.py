import models.model_item as m

print(' * Testing: Item...')

m.add_item(10000, 2, 2)
m.remove_item(1)
m.add_item(10000, 2, 3)
m.update_item_amount(2, 2)
m.add_item(10000, 2, 3)
m.add_item(10000, 3, 4)
m.add_item(10001, 1, 8)
assert len(m.get_items_by_user_id(10000, 'cart')) == 2
assert len(m.get_items_by_user_id(10000, 'all')) == 2
assert len(m.get_items_by_user_id(10000, 'purchased')) == 0
assert len(m.get_items_by_user_id(10001, 'cart')) == 1

print(' ✓ Item has passed all the tests')
