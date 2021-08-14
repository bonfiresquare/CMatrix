import os
import sqlite3 as sqlite
from abc import ABC


class Database (ABC):
    _file = None
    _session = None

    def __init__(self, path):
        self._path = path
        if os.path.exists(path):
            self._session = sqlite.connect(self._path)
        else:
            self._session = sqlite.connect(self._path)
            self.build()

    @staticmethod
    def init(file):
        Database._file = file
        if os.path.exists(Database._file):
            Database.connect()
        else:
            Database.connect()
            Database.build()
        return

    @staticmethod
    def build():
        tables = dict(
            Coin='coin_id CHAR(1) PRIMARY KEY NOT NULL, name CHAR(1) NOT NULL, symbol CHAR(1) NOT NULL, '
                 'type CHAR(1) NOT NULL, rank INT(2) NOT NULL, watch BOOLEAN NOT NULL',
            Account='coin_id CHAR(1) PRIMARY KEY NOT NULL, amount DECIMAL(16) NOT NULL'
        )
        for name in tables.keys():
            query = f'CREATE TABLE {name} ({tables[name]})'
            Database._session.execute(query)
        Database._session.commit()
        return
    
    @staticmethod
    def connect():
        Database._session = sqlite.connect(Database._file)
        return

    @staticmethod
    def close():
        Database._session.commit()
        Database._session.close()
        return

    @staticmethod
    def exec(query, halt=False):
        try:
            response = Database._session.execute(query)
            Database._session.commit()
        except Exception as exception:
            if halt:
                raise exception
            else:
                print(f"Error while processing:\n\tQuery: '{query}'\n\tError: '{exception}'")
                return exception
        data = []
        for row in response:
            data.append(row)
        return data
