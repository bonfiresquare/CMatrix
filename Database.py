import os
import sqlite3 as sqlite


class Database:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not Database.__instance:
            Database.__instance = object.__new__(cls)
        return Database.__instance

    def __init__(self, path):
        self._path = path
        if os.path.exists(path):
            self._session = self.connect()
        else:
            self._session = sqlite.connect(self._path)
            self.build()

    def build(self):
        tables = dict(
            Coin='coin_id CHAR(2) PRIMARY KEY NOT NULL, name CHAR(2) NOT NULL, symbol CHAR(1) NOT NULL, type CHAR(1) NOT NULL',
            Account='coin_id CHAR(2) PRIMARY KEY NOT NULL, amount DECIMAL(16) NOT NULL'
        )
        for name in tables.keys():
            query = f'CREATE TABLE {name} ({tables[name]})'
            self._session.execute(query)
        self._session.commit()

    def terminate(self):
        self._session.commit()
        self._session.close()
        self._session = None
        self.__instance = None

    def get_coin(self, coin_id):
        query = f'SELECT * FROM Coin WHERE coin_id = "{coin_id}"'
        data = []
        for row in self._session.execute(query):
            data.append(row)
        return data

    def add_coin(self, coin_id, name, symbol, type):
        query = f'INSERT INTO Coin VALUES ("{coin_id}", "{name}", "{symbol}", "{type}")'
        try:
            self._session.execute(query)
        except sqlite.IntegrityError as e:
            print(f'Integrity error for query \'{query}\':\n\t{e}')
        finally:
            self._session.commit()


