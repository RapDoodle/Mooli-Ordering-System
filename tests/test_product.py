import models.model_product as m
import controllers.controller_product as c
from decimal import Decimal

print('[UNIT TESTING] Testing: Product...')

# The list of products should be empty
# assert len(c.list_categories()) == 0
assert c.add_product(product_name = 'Milk Tea',
                description = 'The original flavor of milk tea.',
                categories = [1, 2],
                price = '9.99',
                priority = '10',
                picture_uuid = '6cbb04d1-0215-469d-b107-6a45e0ffebbf',
                thumbnail_uuid = 'f6d6ba20-52dd-418e-9071-dfd93d62dd76') ==  {'message': 'The product has been added successfully.'}
m.add_product(product_name = 'Green Milk Tea',
                description = 'Also known as the golden milk green.',
                categories = [2],
                price = '12.99',
                priority = '9',
                picture_uuid = '277b7f0c-a992-4579-a812-2fb11000d462',
                thumbnail_uuid = '0d7915fe-8cb1-467a-9457-f46a86a90cf3')
m.add_product(product_name = 'Chocolate Milk Tea',
                description = 'Also known as the golden milk green.',
                categories = [2],
                price = '12.99',
                priority = '8',
                picture_uuid = 'a93e457b-4dc1-417c-b2f3-22d368bf3748',
                thumbnail_uuid = 'dc2a8b2b-e087-4050-bbe0-85303b4f6f1d')
m.add_product(product_name = 'Bubble Chocolate',
                description = 'The chocolate milk tea with bubbles.',
                categories = [1, 2],
                price = '12.99',
                priority = '8',
                picture_uuid = 'cef7fb5c-c4c1-4197-aa0e-423ad1bdefec',
                thumbnail_uuid = 'c544da03-beaf-4f84-a5f1-014bc15ffa8e')
m.add_product(product_name = 'Coffee',
                description = 'Coffee with the original flavor',
                categories = [1, 3],
                price = '18.99',
                priority = '12',
                picture_uuid = 'cef7fb5c-c4c1-4197-aa0e-423ad1bdefec',
                thumbnail_uuid = 'c544da03-beaf-4f84-a5f1-014bc15ffa8e')
m.add_product(product_name = 'Iced Pineapple Matcha',
                description = 'Coffee with the original flavor',
                categories = [5, 6],
                price = '22.99',
                priority = '12',
                picture_uuid = '4f192478-78b9-4f4c-bebd-196ccfa2cd68',
                thumbnail_uuid = '927f24b3-dca8-413e-be17-639f995c785b')
m.add_product(product_name = 'Lemon Iced Tea',
                description = 'Enjoy the icy summer.',
                categories = [5],
                price = '16.99',
                priority = '12',
                picture_uuid = '4f192478-78b9-4f4c-bebd-196ccfa2cd68',
                thumbnail_uuid = '927f24b3-dca8-413e-be17-639f995c785b')
m.add_product(product_name = 'Ceylon Black Tea',
                description = 'Ceylon Black Tea',
                categories = [6],
                price = '24.99',
                priority = '12',
                picture_uuid = '4f192478-78b9-4f4c-bebd-196ccfa2cd68',
                thumbnail_uuid = '927f24b3-dca8-413e-be17-639f995c785b')
m.add_product(product_name = 'Jasmine Green Tea',
                description = 'Jasmine Green Tea',
                categories = [6],
                price = '24.99',
                priority = '12',
                picture_uuid = '4f192478-78b9-4f4c-bebd-196ccfa2cd68',
                thumbnail_uuid = '927f24b3-dca8-413e-be17-639f995c785b')
m.update_product(product_id = '9',
                product_name = 'Jasmine Green Tea',
                description = 'With Jasmine Green Tea, enjoy your afternoon.',
                categories = [6],
                price = '25.99',
                priority = '2',
                picture_uuid = '4f192478-78b9-4f4c-bebd-196ccfa2cd67',
                thumbnail_uuid = '927f24b3-dca8-413e-be17-639f995c785c'
                )
assert c.get_product_by_name('Jasmine Green Tea') == {'product_id': 9, 'product_name': 'Jasmine Green Tea', 'description': 'With Jasmine Green Tea, enjoy your afternoon.', 'price': Decimal('25.99'), 'rating': None, 'thumbnail_uuid': '927f24b3-dca8-413e-be17-639f995c785c', 'picture_uuid': '4f192478-78b9-4f4c-bebd-196ccfa2cd67', 'priority': 2}
assert c.get_product_by_product_id('9') == {'product_id': 9, 'product_name': 'Jasmine Green Tea', 'description': 'With Jasmine Green Tea, enjoy your afternoon.', 'price': Decimal('25.99'), 'rating': None, 'thumbnail_uuid': '927f24b3-dca8-413e-be17-639f995c785c', 'picture_uuid': '4f192478-78b9-4f4c-bebd-196ccfa2cd67', 'priority': 2}
assert c.add_product(product_name = 'Dummy',
                description = 'Dummy',
                categories = [1],
                price = '24.99',
                priority = '12') == {'message': 'The product has been added successfully.'}
assert m.find_product(method='product_name', param='Dummy') == {'product_id': 10, 'product_name': 'Dummy', 'description': 'Dummy', 'price': Decimal('24.99'), 'rating': None, 'thumbnail_uuid': '', 'picture_uuid': '', 'priority': 12}
assert len(c.get_all_products()) == 10
assert c.remove_product('10') == {'message': 'The product has been removed successfully.'}
assert len(c.get_all_products()) == 9

print('[UNIT TESTING] Product has passed all the tests')
