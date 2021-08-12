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

    # collect information for coins of interest
    for coin_id in c['coins']:
        if not db.get_coin(coin_id):
            _json = api.get_coin(coin_id)
            if 'error' not in _json.keys():
                db.add_coin(_json['id'], _json['name'], _json['symbol'], _json['type'])
            else:
                print(f"'{coin_id}': {_json['error']}")
        else:
            print (f"'{coin_id}' already in database")

    # while True:
        # todo: fancy processing on database

        # todo: show information of processing and 'the matrix'

        # sleep interval
        # sleep(60/c['runtime']['refreshrate'])

    # output exit information
    print("\nexit program")


if __name__ == "__main__":
    # run in console:
    # python cmdline_args.py --period 10 --fileName 'config.yml'
    main()
