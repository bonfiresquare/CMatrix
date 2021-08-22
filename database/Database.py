from typing import Union
from database import functions
from database import structure
import os
import sqlite3 as sqlite


class Database:
    fnc = functions
    str = structure
    Columns = None
    _file = None
    _conn: sqlite.Connection = None

    @staticmethod
    def init(file):
        Database._file = file
        if os.path.exists(Database._file):
            Database.connect()
        else:
            Database.connect()
            Database.exec('PRAGMA foreign_keys = ON')
            Database.str.build()
        Database.exec('PRAGMA temp_store = 2')
        Database.load_schema()
        return
    
    @staticmethod
    def load_schema():
        tables = list(item[0] for item in Database.exec('select tbl_name from sqlite_master WHERE type = "table"'))
        Database.Columns = {t:list(item[1].lower() for item in Database.exec(f'PRAGMA table_info("{t}")')) for t in tables}
        return

    @staticmethod
    def connect():
        Database._conn = sqlite.connect(Database._file)
        return

    @staticmethod
    def close():
        Database.commit()
        Database._conn.close()
        return

    @staticmethod
    def commit():
        Database._conn.commit()
        return

    @staticmethod
    def exec(query, params = (), *,commit = False, halt=False) -> Union[Exception, list]:
        try:
            response = Database._conn.execute(query, params)
        except Exception as exception:
            if halt:
                raise exception
            else:
                print(f"\nError while processing:\n\tQuery: '{query}'\n\tError: '{exception}'\n")
                return exception
        if commit and response.connection.in_transaction:
            Database.commit()
        return response.fetchall()
    
    @staticmethod
    def enable_foreign_keys():
        Database.exec('PRAGMA foreign_keys = ON', forcecommit=True)
        return
