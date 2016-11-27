from __future__ import absolute_import

from .graph_spec import spec
from .data import get_data

from model_building.build import build_model
from keras.callbacks import TensorBoard

model = build_model(spec)

data = get_data()

train_data = data['train']
test_data = data['test']

model.fit(
    data['train']['in'],
    data['train']['out'],
    nb_epoch=2,
    batch_size=32,
    callbacks=[TensorBoard(log_dir='/tmp/graph-logs')]
)
