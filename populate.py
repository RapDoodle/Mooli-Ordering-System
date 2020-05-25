# Populate the database with fake data for testing
import utils.config_manager
from models.DAO import DAO

print('Creating categories...')
from controllers.controller_category import add_category
add_category('Trending', 12)
add_category('Milk Tea', 11)
add_category('Black Tea', 6)
add_category('Green Tea', 5)
add_category('Fruity', 10)
add_category('Seasonal', 9)

print('Inserting products...')
from controllers.controller_product import add_product
add_product('Milk Tea', [1, 2], 12.99, 12, 'The same milk tea that you must love.')
add_product('Green Milk Tea', [1, 2], 12.99, 10, 'Green milk tea.')
add_product('Chocolate', [2], 12.99, 9, 'Milk tea and chocolate mixing together.')
add_product('Bubble Milk Tea', [1, 2], 13.99, 9, 'The milk tea with bubbles.')
add_product('Herb Jelly Milk Tea', [2], 13.99, 8, 'The milk tea mixed with herb, jelly.')
add_product('Ceylon Black Tea', [3], 8.99, 7, 'The ceylon black tea.')
add_product('Jasmine Green Tea', [4], 8.99, 4, 'The famous Jasmine Green Tea')
add_product('Lemon Iced Tea', [1, 5, 6], 14.99, 2, 'Cooler your summer.')
add_product('Lychee Juice', [1, 5, 6], 15.99, 6, 'Do you know Guangdong is also famous for Lychee.')
add_product('Mango Yougurt', [1, 5, 6], 15.99, 9, 'Yougurt with mangos in it.')
add_product('Apple Crystal', [5, 6], 12.99, 9, 'Milk tea and chocolate mixing together.')

# Setup the enrionment
from controllers.controller_staff import add_staff
from controllers.controller_user import sign_up

import random
from faker import Faker
faker = Faker()

print('Generating 500 real staffs...')
# Generate 500 staffs with real password
print('Generating 500 staffs with real password...')
for i in range(1, 101):
    first_name = faker.first_name()
    last_name = faker.last_name()
    add_staff(
        username = first_name.lower() + last_name.lower(), 
        first_name = first_name,
        last_name = last_name,
        email = faker.email(), 
        password = 'Testpassword123', 
        role_id = random.randint(1,6)
    )

print('Generating 50000 fake users...')
def create_user_bypass(username, email, password, first_name = '', last_name = '', gender = '', phone = ''):
    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    password_hash = b'123'

    sql = """INSERT INTO user(
                username,
                email,
                password_hash,
                first_name,
                last_name,
                gender,
                phone
            ) VALUES (
                %(username)s,
                %(email)s,
                %(password_hash)s,
                %(first_name)s,
                %(last_name)s,
                %(gender)s,
                %(phone)s
            )"""
    cursor.execute(sql, {'username': username,
                    'email': email,
                    'password_hash': password_hash,
                    'first_name': first_name,
                    'last_name': last_name,
                    'gender': gender,
                    'phone': phone
                    })
    cursor.execute('SELECT LAST_INSERT_ID()')
    user_id = cursor.fetchone()['LAST_INSERT_ID()']
    dao.commit()

for i in range(1, 50000):
    first_name = faker.first_name()
    last_name = faker.last_name()
    try:
        create_user_bypass(
            username = first_name.lower() + last_name.lower() + str(random.randint(1000, 10000)), 
            first_name = first_name,
            last_name = last_name,
            email = faker.email(), 
            password = 'Testpassword123'
        )
    except Exception as e:
        print(str(e))

# Populate cart item
print('Generating 100000 times of adding to cart...')
from controllers.controller_cart_item import create_cart_item
for i in range(1, 50000):
    create_cart_item(
        user_id = random.randint(10000,50000),
        product_id = random.randint(1, 12),
        amount = 1
    )
    
dao = DAO()
cursor = dao.cursor()
cursor.execute('UPDATE user SET balance = 50000')

print('Placing orders...')
from controllers.controller_order import place_order
for i in range(10000, 55000):
    place_order(user_id=i, payment='balance')

from models.model_archive import get_archive_index
print('Populating archive...')
for i in range(1, 60000):
    get_archive_index(faker.address() + str(random.randint(10000,50000)))

print('Done.')

