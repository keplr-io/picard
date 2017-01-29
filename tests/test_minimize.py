from __future__ import absolute_import
import unittest

from picard.minimizer import get_min_model
from picard.util.data import get_picard_input
from .resource.hyperspec import hyperspec
from .resource.dataspec import dataspec

from hyperopt import Trials
import numpy as np

class TestMinimize(unittest.TestCase):

    def test_minimize(self):
        min_result = get_min_model(
            {
                'data': dataspec,
                'space': hyperspec
            },
            data=get_picard_input(
                dataspec, {
                    'title': np.loadtxt('./tests/resource/datain.csv'),
                    'score': np.loadtxt('./tests/resource/dataout.csv')
                }
            ),
            trials=Trials(),
            max_evals=1
        )

        self.assertEquals(
            type(min_result),
            dict
        )
