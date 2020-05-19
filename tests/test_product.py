import models.model_product as m
import controllers.controller_product as c
from decimal import Decimal

print(' * Testing: Product...')

# The list of products should be empty
assert c.add_product(product_name = 'Milk Tea',
                description = 'The original flavor of milk tea.',
                categories = [1, 2],
                price = '9.99',
                priority = '10') ==  {'status': 200}
m.add_product(product_name = 'Green Milk Tea',
                description = 'Also known as the golden milk green.',
                categories = [2],
                price = '12.99',
                priority = '9')
m.add_product(product_name = 'Chocolate Milk Tea',
                description = 'Also known as the golden milk green.',
                categories = [2],
                price = '12.99',
                priority = '8')
m.add_product(product_name = 'Bubble Chocolate',
                description = 'The chocolate milk tea with bubbles.',
                categories = [1, 2],
                price = '12.99',
                priority = '8')
m.add_product(product_name = 'Coffee',
                description = 'Coffee with the original flavor',
                categories = [1, 3],
                price = '18.99',
                priority = '12')
m.add_product(product_name = 'Iced Pineapple Matcha',
                description = 'Coffee with the original flavor',
                categories = [5, 6],
                price = '22.99',
                priority = '12')
m.add_product(product_name = 'Lemon Iced Tea',
                description = 'Enjoy the icy summer.',
                categories = [5],
                price = '16.99',
                priority = '12')
m.add_product(product_name = 'Ceylon Black Tea',
                description = 'Ceylon Black Tea',
                categories = [6],
                price = '24.99',
                priority = '12')
m.add_product(product_name = 'Jasmine Green Tea',
                description = 'Jasmine Green Tea',
                categories = [6],
                price = '24.99',
                priority = '12')
m.update_product(product_id = '9',
                product_name = 'Jasmine Green Tea',
                description = 'With Jasmine Green Tea, enjoy your afternoon.',
                categories = [6],
                price = '25.99',
                priority = '2')
assert c.get_product_by_name('Jasmine Green Tea') == {'product_id': 9, 'product_name': 'Jasmine Green Tea', 'description': 'With Jasmine Green Tea, enjoy your afternoon.', 'price': Decimal('25.99'), 'priority': 2}
assert c.get_product_by_product_id('9') == {'product_id': 9, 'product_name': 'Jasmine Green Tea', 'description': 'With Jasmine Green Tea, enjoy your afternoon.', 'price': Decimal('25.99'), 'priority': 2}
assert c.add_product(product_name = 'Dummy',
                description = 'Dummy',
                categories = [1],
                price = '24.99',
                priority = '12') == {'status': 200}
assert m.find_product(method='product_name', param='Dummy') == {'product_id': 10, 'product_name': 'Dummy', 'description': 'Dummy', 'price': Decimal('24.99'), 'priority': 12}
assert len(c.get_all_products()) == 10
assert c.remove_product('10') == {'status': 200}
assert len(c.get_all_products()) == 9

print(' ✓ Product has passed all the tests')
