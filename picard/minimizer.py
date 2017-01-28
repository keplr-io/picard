from __future__ import absolute_import

from hyperopt import fmin, tpe
from picard.parser.parse import parse
from picard.builder.build import build_model
from picard.util.file import create_path
from hyperopt import STATUS_OK
import random

def get_min_model(
    spec,
    data=None,
    trials=None,
    training_callback_getters=[],
    start_callback=lambda *x: x,
    end_callback=lambda *x: x,
    algo=tpe.suggest,
    max_evals=5
):
    return fmin(
        get_objective_fn(
            data,
            spec['data'],
            training_callback_getters,
            start_callback,
            end_callback
        ),
        parse(spec['space']),
        trials=trials,
        algo=algo,
        max_evals=max_evals,
    )

def get_objective_fn(
    data,
    data_config,
    training_callback_getters,
    start_callback,
    end_callback
):
    def objective(model_config):
        model = build_model(model_config, data_config)

        model_key = str(id(model_config)) + str(random.random())

        start_callback(model_key)

        model.fit(
            data['train']['in'],
            data['train']['out'],
            validation_split=data_config['training']['val_split'],
            nb_epoch=data_config['training']['epochs'],
            verbose=1,
            callbacks=[
                getter(model_key)
                for getter in training_callback_getters
            ],
            **(model_config['fit'])
        )

        loss = sum(model.evaluate(
            data['test']['in'],
            data['test']['out'],
            verbose=1,
        ))

        model_filename = model_key +'.h5'

        model_file_path = 'model_exports/' + model_filename
        create_path(model_file_path)
        model.save(model_file_path)

        model_result = {
            'loss': loss,
            'status': STATUS_OK,
            'model_config': model_config,
            'model_file': model_filename,
            'model_key': model_key
        }

        end_callback(
            model_key,
            model_result,
            model_file_path
        )

        return model_result

    return objective

