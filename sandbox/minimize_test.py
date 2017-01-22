from __future__ import absolute_import

from picard.search.minimizer import Minimizer

from graph_hyperspec import hyperspec
from data import get_data
from hyperopt import Trials
from data_spec import data_spec
import numpy as np
np.random.seed(1337)  # for reproducibility

minimizer = Minimizer(
    'experiment',
    'lol',
    data_config=data_spec,
    space_config=hyperspec,
    data=get_data(),
    trials=Trials()
)

minModel = minimizer.get_min_model(max_evals=10)

print('test result')
print(minModel)
