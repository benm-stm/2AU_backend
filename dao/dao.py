import MySQLdb
import sys
sys.path.append('/root/2AU_python_script')
from myconfig import *

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class DAO(Singleton):
    def __init__(self):
        """
        Inits MySQL connection
        """
        self._connect()


    def _connect(self):
        """
        Creates connection
        """
        self.connection = MySQLdb.connect(host=db_host, \
            user=db_user, \
            passwd=db_passwd, \
            db=db_name, \
            port=int(db_port))

    def _commit(self):
        """
        commit request
        """
        self.connection.commit()

    def _get_cursor(self):
        """
        Pings connection and returns cursor
        """
        try:
            self.connection.ping()
        except:
            self._connect()
        return self.connection.cursor()


    def get_row(self, query):
        """
        Fetchs one row
        """
        cursor = self._get_cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row


    def get_rows(self, query):
        """
        Fetchs all rows
        """
        cursor = self._get_cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows


    def execute(self, query):
        """ 
        Executes query for update, delete
        """
        cursor = self._get_cursor()
        cursor.execute(query)
        self._commit()
        cursor.close()

    def getDao(self):
        return self.connection.cursor()
