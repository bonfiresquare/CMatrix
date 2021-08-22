from api import Api
from config import Config
from database import Database, functions as dbf
from helper import *


class App:
    __instance = None
    __locked = False

    def __new__(cls, *args, **kwargs):
        if not App.__instance:
            App.__instance = object.__new__(cls)
        if not App.__locked:
            App.__locked = True
            return App.__instance
        else:
            raise RuntimeError('Already initiated or running')

    def __init__(self, configfile):
        Config.init(configfile)
        Api.init(Config.runtime.api)
        Database.init(Config.runtime.database)

    def update_coins_from_api(self):
        table = 'Currency'
        table_data = subselect(dbf.select(table,'Id'), [0])
        for coin in Api.get_coin():
            if coin['id'] in table_data:
                dbf.update(table, transpose(coin, table), {'id': coin['id']})
            else:
                dbf.insert(table, transpose(coin, table))
        Database.commit()
        return

    def main(self):
        # dbf.select('Currency', 'Id', {'type': 'coin', 'active': True, 'rank': 1})
        # write coin information from api to database
        self.update_coins_from_api()

        # while True:
            # todo: fancy processing on database

            # todo: show information of processing and 'the matrix'

            # sleep interval
            # sleep(60/Config.runtime.refreshrate)

        Database.close()
        # Config.write()
