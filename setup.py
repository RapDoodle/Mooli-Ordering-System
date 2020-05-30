from cryptography.fernet import Fernet
import pymysql
import cryptography
import json
import os

SECURITY_PATH = './security'
SECURITY_KEY_PATH = './security/key.key'
SECURITY_CONFIG_PATH = './security/config.obj'
CONFIG_PATH = './config.json'
LOG_PATH = './log'

def y_n_choice(msg = 'Do you want to continue?'):
    choice = input(msg + ' [Y/n] ')
    return True if (choice == 'Y' or choice == 'y' or choice == '') else False

def setup():
    # Check if the system has been initialized
    if os.path.exists(CONFIG_PATH):
        print('A configuration is detected, are you sure to continue?')
        print('WARNING: DOING SO WILL RESULT IN THE LOST OF ALL ')
        print('         PREVIOUS CONFIGURATION!')
        print('NOTE: You may want to checkout config.json before reinitializing.')
        if not y_n_choice():
            exit()

    # Promopt the adminstrator for db info
    print('\nPlease enter the URL of the database')
    db_url = input('(Default: 127.0.0.1): ') or '127.0.0.1'
    print('\nPlease enter the username of the database')
    db_username = input('(Default: root): ') or 'root'
    print('\nPlease enter the password of the database')
    db_password = input('(Default: None): ') or ''
    print('\nPlease enter the name of the database')
    db_name = input('(Default: mooli):') or 'mooli'

    # Attempt to connect to the database
    try:
        connection = pymysql.connect(db_url, db_username, db_password)
    except:
        # Incorrect db credential or internal error
        print('\nERROR Unable to connect to database.\n')
        exit()

    init_db(connection, db_name)

    if not os.path.exists(SECURITY_PATH):
        os.mkdir(SECURITY_PATH)

    # Create the path for logging
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)

    # Generate a random key for config encryption
    key = Fernet.generate_key()
    key_file = open(SECURITY_KEY_PATH, 'wb')
    key_file.write(key)
    key_file.close()

    # Write config for security information
    security_profile = {
        'DB_USERNAME': db_username,
        'DB_PASSWORD': db_password,
        'DB_NAME': db_name,
        'SECRET_KEY': str(Fernet.generate_key())
    }
    with open(SECURITY_CONFIG_PATH, 'wb') as encrypted_profile:
        f = Fernet(key)
        encrypted_profile.write(f.encrypt(json.dumps(security_profile).encode()))

    print('\nWould you like to enable HTTPS on your server?')
    print('NOTE: You will need a SSL certificate to use HTTPS.')
    print('WARNING: Certain function will be disabled without HTTPS for')
    print('         security concerns.')
    enable_https = y_n_choice('Your choice ')
    if enable_https:
        print('The default configuration for you SSL certificate location is: ')
        print(' - Certificate Path: ./security/cert.pem')
        print(' - Private Key Path: ./security/privkey.pem')
        print('We recommend storing the TLS cetificates outside the project folder')
        print('For more information, please refer to the READEME included.')
    print('\nPlease enter the port the application will be running on')
    port = ''
    if enable_https:
        port = input('(Default: 443): ') or '443'
    else:
        port = input('(Default: 80): ') or '80'
    print('\nWould you like to disable debugging on your server?')
    print('NOTE: Keep it disabled in production mode.')
    debug = not y_n_choice('Your choice')
    config = {
        'DB_URL': db_url,
        'port': port,
        'enable_https': enable_https,
        'cert_path': './security/cert.pem',
        'private_key_path': './security/privkey.pem',
        'debug': debug
    }

    with open(CONFIG_PATH, 'w') as profile:
        profile.write(json.dumps(config))

    try:
        init_permission_system()
        init_default_role_permission()
    except:
        print('\nAn error ocurred while initializing the permission system.')
        print('It is likely that the system has already been initialized.')

    print('\nWould you like to setup superuser?')
    if y_n_choice('Your choice'):
        finish = False
        while not finish:
            print('\nPlease enter the username of the superuser. (8-24 characters)')
            username = input()
            print('\nPlease enter an email for the superuser.')
            email = input()
            print('\nPlease enter the password for the superuser.')
            print('Requirements:')
            print(' - The length should between 8 to 24 characters')
            print(' - At least one upper case letter')
            print(' - At least one lower case letter')
            print(' - At least one digit')
            password_1 = input()
            print('\nPlease enter the password for the superuser again.')
            password_2 = input()
            if password_1 != password_2:
                print('\nPasswords do not match.')
                continue
            result = create_superuser(username, email, password_1)
            if isinstance(result, dict):
                if 'error' in result:
                    print('ERROR: ' + result['error'])
                continue
            finish = True

    print('\nSetup complted.')

def init_db(connection, db_name):
    cursor = connection.cursor()

    print('\nConnection with database established.\n')

    # Check if the database exists
    cursor.execute("""SHOW DATABASES LIKE %(db_name)s""", {'db_name': db_name})
    if cursor.fetchone() is not None:
        print('The database already exists, are you sure to continue the initialization?')
        print('WARNING: DOING SO WILL RESULT IN THE LOST OF ALL EXISTING DATA!')
        if not y_n_choice():
            return

    # Initialize the database
    cursor.execute('DROP DATABASE IF EXISTS {}'.format(db_name))
    cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
    cursor.execute('USE {}'.format(db_name))

    # Initialize tables
    init_db_tables(connection)

    connection.close()

def init_db_tables(connection):

    print('\nInitiaizing database tables...\n')
    cursor = connection.cursor()

    sqls = [
        """CREATE TABLE IF NOT EXISTS user (
            user_id INT AUTO_INCREMENT,
            username VARCHAR(24) NOT NULL,
            email VARCHAR(254) NOT NULL,
            password_hash BINARY(60) NOT NULL,
            first_name VARCHAR(35),
            last_name VARCHAR(35),
            gender BINARY(1),
            phone VARCHAR(32),
            balance DECIMAL(8,2) DEFAULT 0.0,
            avatar MEDIUMBLOB,
            PRIMARY KEY (user_id),
            UNIQUE (username),
            UNIQUE (email)
            )
        """,
        """ALTER TABLE user AUTO_INCREMENT=10000""",
        """CREATE TABLE IF NOT EXISTS permission (
            permission_id INT AUTO_INCREMENT,
            permission_name VARCHAR(32) NOT NULL,
            PRIMARY KEY (permission_id),
            UNIQUE (permission_name))""",
        """CREATE TABLE IF NOT EXISTS role (
            role_id INT NOT NULL AUTO_INCREMENT,
            role_name VARCHAR(32) NOT NULL,
            PRIMARY KEY (role_id),
            UNIQUE (role_name))""",
        """CREATE TABLE IF NOT EXISTS role_permission (
            role_id INT NOT NULL,
            permission_id INT NOT NULL,
            FOREIGN KEY (role_id) REFERENCES role(role_id),
            FOREIGN KEY (permission_id) REFERENCES permission(permission_id))""",
        """CREATE TABLE IF NOT EXISTS staff (
            user_id INT NOT NULL,
            role_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(user_id),
            FOREIGN KEY (role_id) REFERENCES role(role_id)
            )
        """,
        """CREATE TABLE IF NOT EXISTS category (
            category_id INT AUTO_INCREMENT,
            category_name VARCHAR(32),
            priority INT,
            PRIMARY KEY (category_id),
            UNIQUE(category_name)
            )
        """,
        """CREATE TABLE IF NOT EXISTS product (
            product_id INT AUTO_INCREMENT,
            product_name VARCHAR(64) NOT NULL,
            description VARCHAR(140),
            price DECIMAL(8,2) DEFAULT 0.0,
            priority INT NOT NULL,
            PRIMARY KEY (product_id),
            UNIQUE (product_name)
            )
        """,
        """CREATE TABLE IF NOT EXISTS product_category (
            product_id INT,
            category_id INT,
            FOREIGN KEY (product_id) REFERENCES product(product_id),
            FOREIGN KEY (category_id) REFERENCES category(category_id)
            )
        """,
        """CREATE TABLE IF NOT EXISTS archive (
            archive_index INT AUTO_INCREMENT,
            value VARCHAR(255) UNIQUE,
            PRIMARY KEY (archive_index)
        )
        """,
        """CREATE INDEX idx_arvchive_value ON archive(value)""",
        """CREATE TABLE IF NOT EXISTS `order`(
            order_id INT AUTO_INCREMENT,
            actual_paid DECIMAL(8, 2),
            status ENUM('CANC', 'PEND', 'PROC', 'REDY', 'DONE', 'REFN') DEFAULT 'PEND',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (order_id)
            )
        """,
        """ALTER TABLE `order` AUTO_INCREMENT=10000""",
        """CREATE TABLE IF NOT EXISTS user_order (
            order_id INT,
            user_id INT,
            FOREIGN KEY (order_id) REFERENCES `order`(order_id)
                ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES `user`(user_id)
        )""",
        """CREATE INDEX idx_user_order ON user_order(order_id, user_id)""",
        """CREATE TABLE IF NOT EXISTS cart_item (
            cart_item_id INT AUTO_INCREMENT,
            user_id INT NOT NULL,
            product_id INT,
            amount INT UNSIGNED,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (cart_item_id),
            FOREIGN KEY (user_id) REFERENCES user(user_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id),
            CHECK (amount > 0)
        )""",
        """CREATE INDEX idx_user_cart ON user_order(user_id)""",
        """CREATE TABLE IF NOT EXISTS purchased_item (
            product_name_snapshot INT NOT NULL,
            product_price_snapshot DECIMAL(8, 2) NOT NULL,
            amount INT UNSIGNED NOT NULL,
            order_id INT NOT NULL,
            FOREIGN KEY (product_name_snapshot) REFERENCES archive(archive_index),
            FOREIGN KEY (order_id) REFERENCES `order`(order_id),
            CHECK (amount > 0)
        )""",
        """CREATE INDEX idx_purchased_item ON user_order(order_id)""",
        """CREATE TABLE IF NOT EXISTS coupon (
            coupon_code VARCHAR(32),
            value DECIMAL(8, 2) NOT NULL,
            threshold DECIMAL(8, 2) NOT NULL,
            activate_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            expire_date DATETIME,
            PRIMARY KEY (coupon_code),
            CHECK (value <= threshold)
        )
        """,
        """CREATE TABLE IF NOT EXISTS redeem_card (
            redeem_code CHAR(16),
            value DECIMAL(8, 2),
            PRIMARY KEY (redeem_code)
        )
        """,
        # Triggers
        """CREATE TRIGGER before_delete_role
            BEFORE DELETE
            ON role FOR EACH ROW
            BEGIN
                DELETE FROM role_permission WHERE
                    role_permission.role_id = OLD.role_id;
            END
        """,
        """CREATE TRIGGER before_delete_permission
            BEFORE DELETE
            ON permission FOR EACH ROW
            BEGIN
                DELETE FROM role_permission WHERE
                    role_permission.permission_id = OLD.permission_id;
            END
        """,
        """CREATE TRIGGER before_delete_category
            BEFORE DELETE
            ON category FOR EACH ROW
            BEGIN
                DELETE FROM product_category WHERE
                    product_category.category_id = OLD.category_id;
            END
        """,
        """CREATE TRIGGER after_order_cancelled
            BEFORE DELETE
            ON category FOR EACH ROW
            BEGIN
                DELETE FROM product_category WHERE
                    product_category.category_id = OLD.category_id;
            END
        """
    ]

    for sql in sqls:
        cursor.execute(sql)

    print('All tables have been correctly initialized.')
    connection.commit()

def init_permission_system():
    # For the initialization of database
    import utils.config_manager
    from models.model_role import add_permission
    permissions = ['orders', 'products', 'categories', 'coupons', 'redeem_cards', 'staff']
    for permission in permissions:
        add_permission(permission)
    

def create_superuser(username, email, password):
    # For the initialization of database
    import utils.config_manager
    from controllers.controller_staff import add_staff
    return add_staff(username = username, email = email, password = password, role_id = 1)

def init_default_role_permission():
    import utils.config_manager
    from models.model_role import add_role
    role_permissions = [
        {'role_name': 'Superadmin', 'permissions': [1, 2, 3, 4, 5, 6]},
        {'role_name': 'Product Manager', 'permissions': [2, 3]},
        {'role_name': 'Financial Manager', 'permissions': [4, 5]},
        {'role_name': 'Shop Manager', 'permissions': [1, 2, 3, 4, 5]},
        {'role_name': 'Cook', 'permissions': [1]}
    ]
    for role_permission in role_permissions:
        add_role(
            role_name = role_permission['role_name'],
            permission_ids = role_permission['permissions'])

def init_test_db():
    # Codes for performing unit testing

    # Load configuration
    import utils.config_manager as config_manager

    # Change some configuration of the database temporarily
    config_manager.set_security_temp('DB_NAME', config_manager.get_security('DB_NAME') + '_test')
    config_manager.set_security_temp('UNIT_TESTING_MODE', True)

    connection = pymysql.connect(config_manager.get('DB_URL'),
                                config_manager.get_security('DB_USERNAME'),
                                config_manager.get_security('DB_PASSWORD'))

    connection.cursor().execute('DROP DATABASE IF EXISTS {}'.format(config_manager.get_security('DB_NAME')))
    connection.cursor().execute('CREATE DATABASE IF NOT EXISTS {}'.format(config_manager.get_security('DB_NAME')))
    connection.cursor().execute('USE {}'.format(config_manager.get_security('DB_NAME')))
    init_db_tables(connection)
    connection.close()

if __name__ == '__main__':
    setup()
