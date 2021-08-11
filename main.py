import sys
sys.path.append(".")
import argparse
from time import sleep
import json
from Api import Api


def cli():
    parser = argparse.ArgumentParser(description='CMatrix helps to decide when to switch between currencies.')
    parser.add_argument('--p', type=int, nargs=1, default=10, required=False,
                        help='period of time (days) that should influence the forecast')
    parser.add_argument('--f', type=str, nargs=1, default='settings.json',
                        help='directory of json-file containing coins of interests', required=False)

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
    coi = read_settings(file_name)

    # create the Api
    api = Api(url='https://api.coinpaprika.com/v1/')
    # todo: init database

    # todo: read refreshrate  (maybe from settings or cli)
    refresh_rate = 12 #times per minute

    while True:
        # get some values
        for c in coi:
            tmp_json = api.get_coin(c)
            print(tmp_json['name'] + ": " + str(tmp_json['rank']))

        # todo: save coins in database

        # todo: fancy processing on database

        # todo: show information of processing and 'the matrix'
        sleep(60/refresh_rate)


if __name__ == "__main__":
    # run in console:
    # python cmdline_args.py --period 10 --fileName 'settings.json'
    main()
