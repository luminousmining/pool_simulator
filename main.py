import sys
import argparse
import logging


from utils import ALGORITHM
from core import Pool


LOG_LEVEL = logging.DEBUG
logging.basicConfig(
    format='[%(levelname)s][%(asctime)s]: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    encoding='utf-8',
    level=LOG_LEVEL)


parser = argparse.ArgumentParser(description='')
parser.add_argument('--host',
                    type=str,
                    default='127.0.0.1',
                    help="")
parser.add_argument('--port',
                    type=int,
                    default=7878,
                    help="")
parser.add_argument('--algo',
                    default='ethash',
                    choices=ALGORITHM.values(),
                    help="Mining algorithm to simulate")
parser.add_argument('--workflow-file',
                    type=str,
                    default=None,
                    help="Path to the workflow JSON file (required when --algo workflow)")
parser.add_argument('--workflow-name',
                    type=str,
                    default=None,
                    help="Name of the workflow to run from the JSON file (required when --algo workflow)")

args = parser.parse_args()

if args.algo == 'workflow':
    if args.workflow_file is None or args.workflow_name is None:
        logging.error('--workflow-file and --workflow-name are required when --algo workflow')
        sys.exit(1)

pool = Pool(args.algo, args.host, args.port,
            workflow_file=args.workflow_file,
            workflow_name=args.workflow_name)
pool.bind()
pool.process()
