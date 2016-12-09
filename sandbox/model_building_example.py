from __future__ import absolute_import

from graph_spec import spec
from data import get_data

from picard.model_building.build import build_model
from picard.util.data import get_picard_input


from keras.callbacks import TensorBoard
from data_spec import data_spec

model = build_model(spec, data_spec)

data = get_picard_input(data_spec, './sandbox/data/00_short.csv')

print data

train_data = data['train']
test_data = data['test']


model.fit(
    train_data['in'],
    train_data['out'],
    nb_epoch=2,
    batch_size=32,
    callbacks=[TensorBoard(log_dir='/tmp/graph-logs')]
)
