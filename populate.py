# Populate the database with fake data for testing
import utils.config_manager
from models.DAO import DAO

from controllers.controller_staff import add_staff
from controllers.controller_user import sign_up
from controllers.controller_category import add_category
from controllers.controller_product import add_product
from controllers.controller_cart_item import create_cart_item
from controllers.controller_redeem_card import add_redeem_cards
from controllers.controller_coupon import add_coupon
from models.model_user import hash_password

# Random
import random
from faker import Faker
faker = Faker()

# Parameters
NUM_STAFF = 500
NUM_USERS = 50000
NUM_CART_ITEMS = 140000
NUM_ORDERS = 70000
NUM_ARCHIVE = 150000
NUM_REDEEM_CARDS = 100000
NUM_COUPONS = 10000

def populate_categories():
    print('Creating categories...')
    add_category('Trending', 12)
    add_category('Milk Tea', 11)
    add_category('Black Tea', 6)
    add_category('Green Tea', 5)
    add_category('Fruity', 10)
    add_category('Seasonal', 9)

def populate_products():
    print('Inserting products...')
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

def populate_staff():
    print('Generating ' + str(NUM_STAFF) + ' staff...')
    for i in range(1, NUM_STAFF + 1):

        if (i % 10 == 0):
            print('Current progress: ' + str(i) + '/' + str(NUM_STAFF), end='\r')

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

def create_user_bypass(username, email, password_hash, cursor, first_name = '', last_name = '', gender = '', phone = ''):
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

def populate_users():
    print('Generating ' + str(NUM_USERS) + ' fake users...')
    pwd = hash_password('Testpassword123')

    dao = DAO()
    cursor = dao.cursor()

    for i in range(1, NUM_USERS + 1):

        first_name = faker.first_name()
        last_name = faker.last_name()

        if (i % 50 == 0):
            print('Current progress: ' + str(i) + '/' + str(NUM_USERS), end='\r')

        try:
            create_user_bypass(
                username = first_name.lower() + last_name.lower() + str(random.randint(1000, 10000)), 
                first_name = first_name,
                last_name = last_name,
                email = str(random.randint(1000, 10000)) + faker.email(), 
                password_hash = pwd,
                cursor = cursor
            )
        except Exception as e:
            print(str(e))

        if i % 1000 == 0:
            dao.commit()

    dao.commit()

def populate_cart_items():
    print('Generating ' + str(NUM_CART_ITEMS) + ' times of adding to cart...')
    for i in range(1, NUM_CART_ITEMS + 1):

        if (i % 50 == 0):
            print('Current progress: ' + str(i) + '/' + str(NUM_CART_ITEMS), end='\r')

        create_cart_item(
            user_id = random.randint(10000,50000),
            product_id = random.randint(1, 12),
            amount = random.randint(1,5)
        )
    
def set_balance():
    dao = DAO()
    cursor = dao.cursor()
    cursor.execute('UPDATE user SET balance = 50000')
    dao.commit()

def populate_orders():
    print('Placing orders...')
    from controllers.controller_order import place_order
    for i in range(10000, 10000 + NUM_ORDERS + 1):

        if (i % 50 == 0):
            print('Current progress: ' + str(i) + '/' + str(NUM_ORDERS), end='\r')

        place_order(user_id=i)

def get_archive_index(value, cursor):
    # Clean input data
    value = str(value).strip()

    search_sql = """SELECT archive_index FROM archive WHERE value = %(value)s"""
    cursor.execute(search_sql, {'value': value})
    result = cursor.fetchone()

    if result is not None:
        return result['archive_index']

    # When the archive library does not exist the given value, create on
    insert_sql = """INSERT INTO archive (value) VALUES (%(value)s)"""
    cursor.execute(insert_sql, {'value': value})

def populate_archive():
    print('Populating archive with ' + str(NUM_ARCHIVE) + ' number of archive records...')
    dao = DAO()
    cursor = dao.cursor()
    for i in range(1, NUM_ARCHIVE + 1):

        if (i % 100 == 0):
            print('Current progress: ' + str(i) + '/' + str(NUM_ARCHIVE), end='\r')

        get_archive_index(faker.address() + str(random.randint(10000,50000)), cursor)

        if (i % 2000 == 0):
            dao.commit()
    
    dao.commit()

def update_state():
    dao = DAO()
    cursor = dao.cursor()
    cursor.execute("""UPDATE `order` SET status = 'DONE'""")
    dao.commit()

def populate_redeem_cards():
    print('Populating redeem_card with ' + str(NUM_REDEEM_CARDS) + ' records...')
    add_redeem_cards(100, NUM_REDEEM_CARDS)

def populate_coupon():
    print('Populating coupon with ' + str(NUM_COUPONS) + ' records...')
    add_coupon('SUMMERSALE', 5, 20, '2020-5-30', '2020-8-30')
    add_coupon('520ILOVEU', 25, 100, '2020-5-20 00:00:00', '2020-5-20 23:59:59')
    add_coupon('MISSU2019', 10, 100, '2019-12-20 00:00:00', '2019-12-31 23:59:59')
    for i in range(1, NUM_COUPONS + 1):
        if (i % 20 == 0):
            print('Current progress: ' + str(i) + '/' + str(NUM_COUPONS), end='\r')

        add_coupon('TESTCOUPON' + str(i), 10, 100, '2020-01-01 00:00:00', '2020-12-31 23:59:59')

if __name__ == '__main__':
    populate_categories()
    populate_products()
    populate_staff()
    populate_users()
    populate_cart_items()
    set_balance()
    populate_orders()
    populate_archive()
    populate_redeem_cards()
    update_state()
    populate_coupon()
    print('Done.')

