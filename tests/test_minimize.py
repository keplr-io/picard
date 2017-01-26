from __future__ import absolute_import
import unittest

from picard.minimizer import Minimizer
from picard.util.data import get_picard_input
from .resource.hyperspec import hyperspec
from .resource.dataspec import dataspec

from pandas import read_csv
from hyperopt import Trials
from keras.preprocessing.text import Tokenizer

df = read_csv('./tests/resource/data.csv')

class TestMinimize(unittest.TestCase):

    def test_minimize(self):
        minimizer = Minimizer(
            spec = {
                'data': dataspec,
                'space': hyperspec
            },
            data=get_picard_input(
                dataspec, {
                    'title': get_input_data(df['title']),
                    'score': df['score'].as_matrix()
                }
            ),
            trials=Trials()
        )

        min_result = minimizer.get_min_model(max_evals=1)
        self.assertEquals(
            type(min_result),
            dict
        )
        self.assertEquals(
            sorted(min_result.keys()),
            sorted([
                'loss',
                'model_config',
                'model_file',
                'model_key',
                'status'
            ])
        )

def get_input_data(frame):
    texts = frame.tolist()
    tokenizer = Tokenizer(nb_words=500)
    tokenizer.fit_on_texts(texts)
    return tokenizer.texts_to_matrix(texts, 'count')