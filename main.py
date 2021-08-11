import sys
sys.path.append(".")
import argparse
from time import sleep
import json
from Api import Api
from Database import Database


def cli():
    parser = argparse.ArgumentParser(description='CMatrix helps to decide when to switch between currencies.')
    parser.add_argument('--p', type=int, nargs=1, default=10, required=False,
                        help='period of time (days) that should influence the forecast')
    parser.add_argument('--f', type=str, nargs=1, default='settings.json',
                        help='directory of json-file containing runtime related settings', required=False)

    args = parser.parse_args()
    return args.p, args.f


def read_settings(filename):
    # read the settings-file
    with open(filename) as jsonFile:
        content = json.load(jsonFile)
        jsonFile.close()
    coi = content['coinsOfInterest']
    return coi


def main():
    # get parameters from command line
    period, file_name = cli()
    # read settings
    coi = read_settings(file_name[0])

    # create the Api
    api = Api(url='https://api.coinpaprika.com/v1/')
    db = Database('data.sqlite')

    # collect coin information
    for id in coi:
        if not db.get_coin(id):
            _json = api.get_coin(id)
            if 'error' not in _json.keys():
                db.add_coin(_json['id'], _json['name'], _json['symbol'], _json['type'])
            else:
                print(f"'{id}': {_json['error']}")
        else:
            print (f"'{id}' already in database")

    # todo: read refreshrate  (maybe from settings or cli)
    refresh_rate = 12 #times per minute

    # while True:
        # todo: fancy processing on database

        # todo: show information of processing and 'the matrix'
        # sleep(60/refresh_rate)


if __name__ == "__main__":
    # run in console:
    # python cmdline_args.py --period 10 --fileName 'settings.json'
    main()
