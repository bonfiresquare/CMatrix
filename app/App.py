from api import Api
from config import Config
from database import Database as DB
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
        DB.init(Config.runtime.database)

    def get_coins_from_api(self):
        table = 'Coin'
        data = subselect(DB.f.get_coins('coin_id'), [0])
        params= []
        for coin in Api.get_coin():
            if coin['id'] not in data:
                params.append(values(select(coin, ['id','name','symbol','type'])) + [0])
        if params:
            DB.exec( f"INSERT INTO '{table}' VALUES (?,?,?,?,?)", params, many=True)
        return

    def update_watchlist(self):
        table = 'Coin'
        remaining_watchlist = Config.coins.watchlist.copy()
        data = DB.f.get_coins('coin_id', 'watch', 1)
        if data:
            for coin in data:
                if coin[0] not in remaining_watchlist:
                    DB.exec(f"UPDATE {table} SET watch = 0 WHERE coin_id = '{coin[0]}'")
                else:
                    remaining_watchlist.remove(coin[0])
        for coin_id in remaining_watchlist:
            DB.exec(f"UPDATE {table} SET watch = 1 WHERE coin_id = '{coin_id}'")
        return


    def main(self):
        
        # write coin information from api to database
        self.get_coins_from_api()
        # update watchlist in database
        self.update_watchlist()

        # while True:
            # todo: fancy processing on database

            # todo: show information of processing and 'the matrix'

            # sleep interval
            # sleep(60/Config.runtime.refreshrate)

        DB.close()
        # Config.write()
