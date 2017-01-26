from __future__ import absolute_import

import random
from hyperopt import fmin, tpe, STATUS_OK
from picard.util.file import create_path
from picard.parser.parse import parse
from picard.builder.build import build_model

class Minimizer(object):
    '''
        An experiment determined by
            - training & testing data
            - a search space
            - a hyperopt trials object
    '''

    def __init__(
        self,
        spec,
        data=None,
        trials=None,
        training_callback_getters=[],
        start_callback=lambda *x: x,
        end_callback=lambda *x: x,
    ):
        self.data = data
        self.space = parse(spec['space'])
        self.trials = trials
        self.data_config = spec['data']
        self.start_callback = start_callback
        self.end_callback = end_callback
        self.training_callback_getters = training_callback_getters

    def eval_model(self, model_config):
        '''
            train model on data
        '''

        model = build_model(model_config, self.data_config)

        model_key = str(id(model_config)) + str(random.random())

        self.start_callback(model_key)

        model.fit(
            self.data['train']['in'],
            self.data['train']['out'],
            validation_split=0.3,
            nb_epoch=1,
            verbose=1,
            callbacks=[
                getter(model_key)
                for getter in self.training_callback_getters
            ],
            **(model_config['fit'])
        )

        loss = sum(model.evaluate(
            self.data['test']['in'],
            self.data['test']['out'],
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

        self.end_callback(
            model_key,
            model_result,
            model_file_path
        )

        return model_result


    def get_min_model(self, algo=tpe.suggest, max_evals=5):

        return get_min_trial(
            fmin(
                self.eval_model,
                space=self.space,
                trials=self.trials,
                algo=algo,
                max_evals=max_evals,
            ),
            self.trials
        )['result']

def get_min_trial(search_params, trials):

    for trial in trials:

        params = trial['misc']['vals']

        for key in params.keys():
            if not params[key]:
                params.pop(key, None)
            else:
                params[key] = params[key][0]

        if params == search_params:
            return trial
