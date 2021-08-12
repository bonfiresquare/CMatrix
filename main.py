import sys
import argparse
import yaml
from time import sleep
from Api import Api
from Database import Database

sys.path.append(".")

def cli():
    parser = argparse.ArgumentParser(description='CMatrix helps to decide when to switch between currencies.')
    parser.add_argument('--p', type=int, nargs=1, default=10, required=False,
                        help='period of time (days) that should influence the forecast')
    parser.add_argument('--f', type=str, nargs=1, default='config.yml',
                        help='directory of json-file containing runtime related settings', required=False)

    args = parser.parse_args()
    return args.p, args.f


def load_cofig(path):
    # read the config file
    with open(path, 'r') as content:
        return yaml.safe_load(content)


def main():
    # initialize runtime parameters and objects
    period, configfile = cli()
    c = load_cofig(configfile[0])
    api = Api(c['runtime']['api'])
    db = Database(c['runtime']['database'])

    # collect information for coins
    table = 'Coin'
    data = db.exec(f"SELECT coin_id FROM '{table}'")
    for coin in api.get_coins():
        if coin['rank'] > c['coins']['maxrank']:
            break
        if (coin['id'],) not in data:
            db.exec(f"INSERT INTO '{table}' VALUES ('{coin['id']}', '{coin['name']}', '{coin['symbol']}', '{coin['type']}', '{coin['rank']}', 0)")

    # update watchlist in database
    table = 'Coin'
    remaining_watchlist = c['coins']['watchlist']
    data = db.exec(f"SELECT coin_id from {table} WHERE watch = 1")
    if data:
        for coin in data:
            if coin[0] not in remaining_watchlist:
                db.exec(f"UPDATE {table} SET watch = 0 WHERE coin_id = '{coin[0]}'")
            else:
                remaining_watchlist.remove(coin[0])
    for coin_id in remaining_watchlist:
        db.exec(f"UPDATE {table} SET watch = 1 WHERE coin_id = '{coin_id}'")

    # while True:
        # todo: fancy processing on database

        # todo: show information of processing and 'the matrix'

        # sleep interval
        # sleep(60/c['runtime']['refreshrate'])

    db.terminate()


if __name__ == "__main__":
    # run in console:
    # python cmdline_args.py --period 10 --fileName 'config.yml'

    main()

    # output exit information
    print("\nexit program")
