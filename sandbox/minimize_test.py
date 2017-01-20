from __future__ import absolute_import

from picard.search.minimizer import Minimizer

from graph_hyperspec import hyperspec
from data import get_data
from hyperopt import Trials


minimizer = Minimizer(
    'experiment',
    'lol',
    data_config={'in':[], 'out': []},
    space_config=hyperspec,
    data=get_data(),
    trials=Trials()
)

minModel = minimizer.get_min_model(max_evals=1)

print(minModel)
