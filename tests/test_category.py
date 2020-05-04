import controllers.controller_category as c

print('[UNIT TESTING] Testing: Category...')

# The list of category should be empty
assert len(c.list_categories()) == 0
# Addomg a new category
assert c.add_category('Trending', '6') == {'message': 'The category has been added successfully.'}
# Adding a new category with the same name
assert c.add_category('trending', '5') == {'error': 'The category already exists.'}
# Adding a new category with a different name
assert c.add_category('Tea', '2') == {'message': 'The category has been added successfully.'}
assert c.add_category('Coffee', '3') == {'message': 'The category has been added successfully.'}
# A new category with the same name
assert c.add_category('Summer', '3') == {'message': 'The category has been added successfully.'}
assert c.list_categories() == [
    {'category_id': 1, 'category_name': 'Trending', 'priority': 6},
    {'category_id': 3, 'category_name': 'Coffee', 'priority': 3},
    {'category_id': 4, 'category_name': 'Summer', 'priority': 3},
    {'category_id': 2, 'category_name': 'Tea', 'priority': 2}
]
# Adding a category without name and priorty respectively
assert c.add_category('', '3') == {'error': 'Invalid input type.'}
assert c.add_category('New', '') == {'error': 'Invalid input type.'}

print('[UNIT TESTING] Category has passed all the tests')
