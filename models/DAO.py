import utils.config_manager as config
import pymysql

class DAO():

    __db_url = config.get('db_url')
    __db_username = config.get('db_username')
    __db_password = config.get('db_password')
    __db_name = config.get('db_name')
    __db = None

    def __init__(self):
        self.__db = self.db_connect()

    def db_connect(self):
        try:
            self.__db = pymysql.connect(self.__db_url, self.__db_username,
                                        self.__db_password, self.__db_name)
            return self.__db
        except:
            raise Exception('Unable to connect')

    def cursor(self):
        return self.__db.cursor()

    def __del__(self):
        if self.__db is not None:
            self.__db.close()
