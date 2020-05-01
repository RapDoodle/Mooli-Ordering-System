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
        connection = pymysql.connect(db_url, db_username, db_password, db_name)
    except:
        print('Unable to connect to database.')
        exit()

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
            product_id INT UNSIGNED,
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
    ]

    for sql in sqls:
        cursor.execute(sql)

setup()
