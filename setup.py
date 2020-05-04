from cryptography.fernet import Fernet
import pymysql
import cryptography
import json
import os

security_path = './security'
security_key_path = './security/key.key'
config_path = './config.json'

def setup():

    # Check if the system has been initialized
    if os.path.exists(config_path):
        print('A configuration is detected, are you sure to continue?')
        print('[WARNING] DOING SO WILL RESULT IN THE LOST OF PREVIOUS CONFIGURATION!')
        choice = input('Do you want to continue? [Y/n] ')
        if not (choice == 'Y' or choice == 'y'):
            exit()

    # Promopt the adminstrator for db info
    print('Please enter the URL of the database')
    db_url = input('(Default: 127.0.0.1): ') or '127.0.0.1'
    print('Please enter the username of the database')
    db_username = input('(Default: root): ') or 'root'
    print('Please enter the password of the database')
    db_password = input('(Default: None): ') or ''
    print('Please enter the name of the database')
    db_name = input('(Default: mooli):') or 'mooli'

    # Attempt to connect to the database
    try:
        connection = pymysql.connect(db_url, db_username, db_password)
    except:
        # Incorrect db credential or internal error
        print('Unable to connect to database.')
        exit()

    connection.cursor().execute('DROP DATABASE IF EXISTS {}'.format(db_name))
    connection.cursor().execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
    connection.cursor().execute('use {}'.format(db_name))
    print('Connection with database established.')
    init_db_tables(connection)
    connection.close()

    if not os.path.exists(security_path):
        os.mkdir(security_path)

    # Generate a random key for config encryption
    key = Fernet.generate_key()
    key_file = open(security_key_path, 'wb')
    key_file.write(key)
    key_file.close()

    # Write config
    profile = {
        'DB_URL': db_url,
        'DB_USERNAME': db_username,
        'DB_PASSWORD': db_password,
        'DB_NAME': db_name,
        'SECRET_KEY': str(Fernet.generate_key())
    }
    with open('config.json', 'wb') as encrypted_profile:
        f = Fernet(key)
        encrypted_profile.write(f.encrypt(json.dumps(profile).encode()))

    print('Setup complted.')

def init_db_tables(connection):

    print('Initiaizing database tables...')
    cursor = connection.cursor()

    sqls = [
        """CREATE TABLE IF NOT EXISTS permission (permission_name VARCHAR(32), group_name VARCHAR(32))""",
        """CREATE TABLE IF NOT EXISTS staff (
            staff_id INT(5) UNSIGNED AUTO_INCREMENT,
            username VARCHAR(30) NOT NULL,
            password_hash BINARY(64) NOT NULL,
            permission_group_name VARCHAR(32),
            PRIMARY KEY (staff_id)
            )
        """,
        """ALTER TABLE staff AUTO_INCREMENT=10000""",
        """CREATE TABLE IF NOT EXISTS customer (
            customer_id INT(8) UNSIGNED AUTO_INCREMENT,
            username VARCHAR(30) NOT NULL,
            password_hash BINARY(64) NOT NULL,
            first_name VARCHAR(35),
            last_name VARCHAR(35),
            gender BINARY(1),
            phone VARCHAR(32),
            balance DECIMAL(8,2),
            PRIMARY KEY (customer_id)
            )
        """,
        """ALTER TABLE customer AUTO_INCREMENT=1000000""",
        """CREATE TABLE IF NOT EXISTS category (
            category_name VARCHAR(32),
            priority INT,
            PRIMARY KEY (category_name)
            )
        """,
        """CREATE TABLE IF NOT EXISTS product (
            product_id INT UNSIGNED AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            category VARCHAR(32) NOT NULL,
            price DECIMAL(8,2) DEFAULT 0.0,
            rating DECIMAL(2,1),
            picture VARCHAR(255),
            priority INT,
            PRIMARY KEY (product_id)
            )
        """,
        """CREATE TABLE IF NOT EXISTS product_category (
            product_id INT UNSIGNED,
            category_name VARCHAR(32),
            FOREIGN KEY (product_id) REFERENCES product(product_id),
            FOREIGN KEY (category_name) REFERENCES category(category_name)
            )
        """,
        """CREATE TABLE IF NOT EXISTS `order`(
            order_id INT UNSIGNED AUTO_INCREMENT,
            total DECIMAL(8, 2),
            discount DECIMAL(8, 2),
            actual_paid DECIMAL(8, 2),
            status INT,
            purchased_date TIMESTAMP,
            PRIMARY KEY (order_id)
            )
        """,
        """CREATE TABLE IF NOT EXISTS item (
            item_id INT UNSIGNED AUTO_INCREMENT,
            customer_id INT(8) UNSIGNED,
            product_id INT UNSIGNED,
            order_id INT UNSIGNED,
            amount INT,
            PRIMARY KEY (item_id),
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id),
            FOREIGN KEY (order_id) REFERENCES `order`(order_id)
        )
        """,
        """CREATE TABLE IF NOT EXISTS coupon (
            coupon_code VARCHAR(32),
            amount DECIMAL(8, 2),
            threshold DECIMAL(3, 2),
            percentage DECIMAL (3, 2),
            PRIMARY KEY (coupon_code)
        )
        """,
        """CREATE TABLE IF NOT EXISTS redeem_card (
            redeem_code CHAR(16),
            amount DECIMAL(8, 2),
            PRIMARY KEY (redeem_code)
        )
        """,
        """CREATE TABLE IF NOT EXISTS comment (
            comment_id INT AUTO_INCREMENT,
            customer_id INT(8) UNSIGNED,
            product_id INT UNSIGNED,
            rating DECIMAL(2,1),
            body VARCHAR(140),
            PRIMARY KEY (comment_id),
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id)
        )
        """,
    ]
    print('=====================================')
    for sql in sqls:
        cursor.execute(sql)

def init_test_db():

    import utils.config_manager as config_manager

    config_manager.set_temp('DB_NAME', config_manager.get('DB_NAME') + '_test')
    config_manager.set_temp('UNIT_TESTING_MODE', True)

    connection = pymysql.connect(config_manager.get('DB_URL'), config_manager.get('DB_USERNAME'), config_manager.get('DB_PASSWORD'))

    connection.cursor().execute('DROP DATABASE IF EXISTS {}'.format(config_manager.get('DB_NAME')))
    connection.cursor().execute('CREATE DATABASE IF NOT EXISTS {}'.format(config_manager.get('DB_NAME')))
    connection.cursor().execute('USE {}'.format(config_manager.get('DB_NAME')))
    init_db_tables(connection)
    connection.close()

if __name__ == '__main__':
    setup()
