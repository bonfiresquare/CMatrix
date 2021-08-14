import argparse
from app import App


def cli():
    parser = argparse.ArgumentParser(description='CMatrix helps to decide when to switch between currencies.')
    parser.add_argument('--p', type=int, nargs=1, default=10, required=False,
                        help='period of time (days) that should influence the forecast')

    args = parser.parse_args()
    return args.p


if __name__ == "__main__":
    # run in console:
    # python cmdline_args.py --period 10 --fileName 'config.yml'

    # initialize runtime parameters and objects
    period = cli()

    # init app and enter main loop
    app = App(configfile='config.yml')
    app.main()

    print("\nexit app")
