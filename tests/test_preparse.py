from __future__ import absolute_import
import unittest
from picard.parser.parse import preparse
from .resource.hyperspec import hyperspec, expected_result

class TestPreparse(unittest.TestCase):

    def test_preparse(self):
        self.assertEqual(preparse(hyperspec), expected_result)
