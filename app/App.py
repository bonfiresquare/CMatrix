import helper as h
from .Api import Api
from .Database import Database
from config import Config


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

    def get_coins_from_api(self):
        table = 'Coin'
        data = Database.exec(f"SELECT coin_id FROM '{table}'")
        for coin in Api.get_coins():
            if coin['rank'] > Config.coins.maxrank:
                break
            if (coin['id'],) not in data:
                Database.exec(
                    f"INSERT INTO '{table}' "
                    f"VALUES ("
                    f"'{coin['id']}', "
                    f"'{coin['name']}', "
                    f"'{coin['symbol']}', "
                    f"'{coin['type']}', "
                    f"'{coin['rank']}', "
                    f"0)"
                )
        return

    def update_watchlist(self):
        table = 'Coin'
        remaining_watchlist = Config.coins.watchlist.copy()
        data = Database.exec(f"SELECT coin_id from {table} WHERE watch = 1")
        if data:
            for coin in data:
                if coin[0] not in remaining_watchlist:
                    Database.exec(f"UPDATE {table} SET watch = 0 WHERE coin_id = '{coin[0]}'")
                else:
                    remaining_watchlist.remove(coin[0])
        for coin_id in remaining_watchlist:
            Database.exec(f"UPDATE {table} SET watch = 1 WHERE coin_id = '{coin_id}'")
        return


    def main(self):

        # test helper function
        h.foo()
        
        # write coin information from api to database
        self.get_coins_from_api()
        # update watchlist in database
        self.update_watchlist()

        # while True:
            # todo: fancy processing on database

            # todo: show information of processing and 'the matrix'

            # sleep interval
            # sleep(60/Config.runtime.refreshrate)

        Database.close()
        Config.write()
