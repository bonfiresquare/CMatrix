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
            self._session = sqlite.connect(self._path)
        else:
            self._session = sqlite.connect(self._path)
            self.build()

    def build(self):
        tables = dict(
            Coin='coin_id CHAR(1) PRIMARY KEY NOT NULL, name CHAR(1) NOT NULL, symbol CHAR(1) NOT NULL, type CHAR(1) NOT NULL, rank INT(2) NOT NULL, watch BOOLEAN NOT NULL',
            Account='coin_id CHAR(1) PRIMARY KEY NOT NULL, amount DECIMAL(16) NOT NULL'
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

    def exec(self, query, halt=False):
        try:
            response = self._session.execute(query)
            self._session.commit()
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
