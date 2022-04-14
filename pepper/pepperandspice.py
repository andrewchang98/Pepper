from datetime import datetime
from utilities.Pepper import Pepper

logger = logging.getLogger()

def main():

if __name__ == '__main__':
    import argparse

    fmt = '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    fh = logging.FileHandler('console.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(fmt))
    logger.addHandler(fh)

    parser = argparse.ArgumentParser()
    parser.add_argument('symbols', nargs='+')
    parser.add_argument('--lot', type=float, default=2000)

    main(parser.parse_args())

pep = Pepper()
