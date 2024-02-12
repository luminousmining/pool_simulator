import sys
import argparse
import logging
import time


from algorithm import is_valid_algorithm
from pool import Pool


log_level = logging.DEBUG
logging.basicConfig(
    format='[%(levelname)s][%(asctime)s]: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    encoding='utf-8',
    level=log_level)


parser = argparse.ArgumentParser(description='')
parser.add_argument('--host',
                    type=str,
                    default='127.0.0.1',
                    help="")
parser.add_argument('--port',
                    type=str,
                    default='7878',
                    help="")
parser.add_argument('--algo',
                    default='ethash',
                    type=str,
                    help="[ethash]")

args = parser.parse_args()

if is_valid_algorithm(args.algo) is False:
    logging.error(f'Algorithm unsupported {args.algo}')
    sys.exit(1)

pool = Pool(args.algo, args.host, int(args.port))
pool.start()
while pool.is_alive() is True:
    pool.on_receive()
    time.sleep(0.1)
