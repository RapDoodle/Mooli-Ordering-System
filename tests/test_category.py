import controllers.controller_category as c

print(' * Testing: Category...')

# The list of category should be empty
assert len(c.list_categories()) == 0
# Addomg a new category
assert c.add_category('Trending', '6') == {'message': 'The category has been added successfully.'}
# Adding a new category with the same name
assert c.add_category('trending', '5') == {'error': 'The category already exists.'}
# Adding a new category with a different name
assert c.add_category('Milk Tea', '2') == {'message': 'The category has been added successfully.'}
assert c.add_category('Wrong Coffee', '3') == {'message': 'The category has been added successfully.'}
# A new category with the same name
assert c.add_category('Summer', '3') == {'message': 'The category has been added successfully.'}
# Add additional categories
assert c.add_category('Fruity', '1') == {'message': 'The category has been added successfully.'}
assert c.add_category('Black & Green', '0') == {'message': 'The category has been added successfully.'}
# Adding a category without name and priorty respectively
assert c.add_category('', '3') == {'error': 'Invalid input type.'}
assert c.add_category('New', '') == {'error': 'Invalid input type.'}

assert c.list_categories() == [
    {'category_id': 1, 'category_name': 'Trending', 'priority': 6},
    {'category_id': 4, 'category_name': 'Summer', 'priority': 3},
    {'category_id': 3, 'category_name': 'Wrong Coffee', 'priority': 3},
    {'category_id': 2, 'category_name': 'Milk Tea', 'priority': 2},
    {'category_id': 5, 'category_name': 'Fruity', 'priority': 1},
    {'category_id': 6, 'category_name': 'Black & Green', 'priority': 0}
]

# Test for update and delete
assert c.update_category('3', 'Coffee', '4') == {'message': 'The category information has been updated.'}
assert c.update_category('8', 'Coffee', '4') == {'error': 'The category does not exists.'}
assert c.add_category('Dummy', '0') == {'message': 'The category has been added successfully.'}
assert c.remove_category('7') == {'message': 'The category has been removed successfully.'}
assert c.remove_category('8') == {'error': 'The category does not exists.'}

print(' ✓ Category has passed all the tests')
