import models.model_item as m

print('[UNIT TESTING] Testing: Item...')

m.add_item(1000000, 2, 2)
m.remove_item(1)
m.add_item(1000000, 2, 3)
m.update_item_amount(2, 2)
m.add_item(1000000, 2, 3)
m.add_item(1000000, 3, 4)
m.add_item(1000001, 1, 8)
assert len(m.get_items_by_user_id(1000000, 'cart')) == 2
assert len(m.get_items_by_user_id(1000000, 'all')) == 2
assert len(m.get_items_by_user_id(1000000, 'purchased')) == 0
assert len(m.get_items_by_user_id(1000001, 'cart')) == 1

print('[UNIT TESTING] Item has passed all the tests')
