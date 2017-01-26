from __future__ import absolute_import, print_function

from pyspark import SparkContext, SparkConf

from picard.search.spark_model import SparkMinimizer

from graph_hyperspec import hyperspec
from data import get_data
from data_spec import data_spec

# from keras import backend as K
# import tensorflow as tf

# K.set_session(tf.Session(
# 	config=tf.ConfigProto(device_count={'GPU': 0})
# ))

conf = SparkConf().setAppName('search ')
context = SparkContext(conf=conf)

spark_model = SparkMinimizer(
    'minimize-exp-search',
    'test-exp',
    data_spec,
    context,
    3
)

spark_model.minimize(
    space=hyperspec,
    data=get_data(),
    search_config={
        'max_evals': 5
    }
)

print(minModel)
