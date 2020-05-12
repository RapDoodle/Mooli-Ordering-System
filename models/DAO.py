import utils.config_manager as config
import pymysql

class DAO():

    __db_url = config.get('DB_URL')
    __db_username = config.get_security('DB_USERNAME')
    __db_password = config.get_security('DB_PASSWORD')
    __db_name = config.get_security('DB_NAME')
    __db = None

    def __init__(self):
        self.__db = self.db_connect()

    def db_connect(self):
        try:
            self.__db = pymysql.connect(host = self.__db_url,
                                        user = self.__db_username,
                                        password = self.__db_password,
                                        db = self.__db_name,
                                        charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor)
            return self.__db
        except:
            raise Exception('Unable to connect')

    def connection(self):
        return self.__db

    def cursor(self):
        return self.__db.cursor()

    def commit(self):
        self.__db.commit()

    def __del__(self):
        if self.__db is not None:
            self.__db.close()

class redisDAO():
    pass
