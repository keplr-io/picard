from __future__ import absolute_import

from pyspark import SparkContext, SparkConf

from picard.model_building.build import build_model
from picard.search.minimizer import Minimizer
from picard.search.spark_model import SparkMinimizer

from graph_hyperspec import hyperspec
from data import get_data

conf = SparkConf().setAppName('lol ')
context = SparkContext(conf=conf)

sparkModel = SparkMinimizer(
    'minimize-exp-search',
    'minimize-exp',
    context,
    3
)

minModel = sparkModel.minimize(
    space=hyperspec,
    data=get_data(),
    search_config={
        'max_evals': 10
    }
)

print(minModel)

