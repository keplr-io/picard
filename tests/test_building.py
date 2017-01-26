from __future__ import absolute_import
import unittest

from picard.builder.build import build_model
from .resource.modelspec import modelspec
from .resource.dataspec import dataspec
from keras.engine.training import Model

class TestBuilding(unittest.TestCase):

    def test_building(self):
        self.assertEqual(
            type(build_model(modelspec, dataspec)),
            Model
        )

