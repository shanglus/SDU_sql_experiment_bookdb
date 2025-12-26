import pymysql
from PySide6.QtWidgets import QMessageBox

class Connector:
    __connection = None
    __cursor = None

    def __init__(self):
        self.__userName = 'root'
        self.__password = '123456'
        self.__databaseName = 'transportdb'
        self.__port = 3306
        try:
            Connector.__connection = pymysql.connect(
                host='localhost',
                user=self.__userName,
                password=self.__password,
                database=self.__databaseName,
                port=self.__port
            )
            Connector.__cursor = Connector.__connection.cursor()
        except Exception as e:
            QMessageBox.critical(None, '错误', f'数据库链接错误: {str(e)}')

    @staticmethod
    def get_cursor():
        if Connector.__connection is not None:
            return Connector.__cursor
        else:
            return None

    @staticmethod
    def get_connection():
        if Connector.__connection is not None:
            return Connector.__connection
        else:
            return None

    @staticmethod
    def close_connection():
        if Connector.__cursor is not None:
            Connector.__cursor.close()
        if Connector.__connection is not None:
            Connector.__connection.close()
        Connector.__connection = None
        Connector.__cursor = None