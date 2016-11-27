from __future__ import absolute_import

from pyspark import SparkContext, SparkConf

from picard.model_building.build import build_model
from picard.search.minimizer import Minimizer
from picard.search.spark_model import SparkMinimizer

from picard.util.data import get_picard_input
from picard.util.s3 import save_s3_file, upload_s3_file, create_path
from picard.spaces.lstm_graph import get_space
import json

def start_search(args):

    print args.model_key
    print args.data_path
    print args.max_evals
    print args.data_config

    data = get_picard_input(
        json.loads(args.data_config),
        save_s3_file(args.data_path)
    )

    conf = SparkConf().setAppName('model-search-' + args.model_key)

    context = SparkContext(conf=conf)

    sparkModel = SparkMinimizer('minimize-' + args.model_key, context)

    print('starting!')


    minModel = sparkModel.minimize(
        space=get_space(args.data_config),
        data=data,
        search_config={
            'max_evals': args.max_evals
        }
    )

    print('done!')

    print minModel


def get_args():

    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='Start a parameter space search.'
    )

    parser.add_argument(
        'model_key',
        type=str,
        help='an identifier for the experiment'
    )

    parser.add_argument(
        'data_path',
        type=str,
        help='an s3:// path to data file'
    )

    parser.add_argument(
        'max_evals',
        type=int,
        default=10,
        help='maximum number of models in searh space to attempt'
    )

    parser.add_argument(
        'data_config',
        type=str,
        help='data fields configuration'
    )

    return parser.parse_args()

if __name__ == '__main__':
    start_search(get_args())
