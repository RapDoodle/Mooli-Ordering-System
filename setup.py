import pymysql

def setup():

    print('Please enter the URL of the database (default: 127.0.0.1): ')
    db_url = input() or '127.0.0.1'
    print('Please enter the username of the database (default: root): ')
    db_username = input() or 'root'
    print('Please enter the password of the database (default: None): ')
    db_password = input() or ''
    print('Please enter the name of the database (default: mooli): ')
    db_name = input() or 'mooli'

    try:
        connection = pymysql.connect(db_url, db_username, db_password)
    except:
        print('Unable to connect to database.')
        exit()

    connection.cursor().execute('DROP DATABASE IF EXISTS {}'.format(db_name))
    connection.cursor().execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
    connection.cursor().execute('use {}'.format(db_name))
    print('Connection with database established.')
    init_db_tables(connection)
    connection.close()
    print('Done')

def init_db_tables(connection):

    print('Initiaizing database tables')
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
            name VARCHAR(32),
            priority INT,
            PRIMARY KEY (name)
        )""",
        """CREATE TABLE IF NOT EXISTS product (
            product_id INT UNSIGNED AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            category VARCHAR(32) NOT NULL,
            price DECIMAL(8,2) DEFAULT 0.0,
            rating DECIMAL(2,1),
            picture VARCHAR(255),
            priority INT,
            PRIMARY KEY (product_id),
            FOREIGN KEY (category) REFERENCES category(name)
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

    for sql in sqls:
        cursor.execute(sql)

setup()
