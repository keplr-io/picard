from __future__ import absolute_import

hyperspec = {

    'operators': {

        'embedding': {
            'operator': 'Embedding',

            'spec': {
                'output_dim': 512,
                'input_dim': 10000,
                'input_length': 100
            }
        },

        'lstm': {
            'operator': 'LSTM',

            'spec': {
                'output_dim': 32
            }
        },

        'dense': {
            'operator': 'Dense',

            'spec': {
                'output_dim': 64,
                'activation': {
                    '$choice': {
                        'options': ['relu', 'sigmoid']
                    }
                }
            }
        },

        'smallDense': {
            'operator': 'Dense',

            'spec': {
                'output_dim': 1,
                'activation': 'sigmoid'
            }
        }

    },

    'legs': {
        'incoming': {
            'headline-input': {
                'shape': (100,),
                'dtype': 'int32'
            },

            'aux-input': {
                'shape': (5,)
            }
        },

        'outgoing': {
            'headline-output': {
                'loss': 'binary_crossentropy',
                'loss_weight': 1.
            },
            'aux-output': {
                'loss': 'binary_crossentropy',
                'loss_weight': 0.2
            }
        }
    },


    'graph': {

        'nodes': [
            'post-embedding',
            'post-lstm',
            'post-dense1',
            'post-dense2',
        ],

        'edges': [
            {
                'source': 'headline-input',
                'target': 'post-embedding',
                'operator': 'embedding'
            },
            {
                'source': 'post-embedding',
                'target': 'post-lstm',
                'operator': 'lstm'
            },
            {
                'source': 'aux-input',
                'target': 'pre-dense',
                'operator': 'IDENTITY'
            },
            {
                'source': 'post-lstm',
                'target': 'pre-dense',
                'operator': 'IDENTITY'
            },
            {
                'source': 'pre-dense',
                'target': 'post-dense1',
                'operator': 'dense'
            },
            {
                'source': 'post-dense1',
                'target': 'post-dense2',
                'operator': 'dense'
            },
            {
                'source': 'post-dense2',
                'target': 'post-dense3',
                'operator': 'dense'
            },
            {
                'source': 'post-dense3',
                'target': 'headline-output',
                'operator': 'smallDense'
            },
            {
                'source': 'post-lstm',
                'target': 'aux-output',
                'operator': 'smallDense'
            },
        ]

    },

    'compile': {
        'optimizer': {
            '$choice': {
                'options': ['rmsprop', 'adam']
            }
        }
    },

    'fit': {
        'batch_size': {
            '$choice': {
                'options': [64, 128]
            }
        },
    }

}

def get_data():

    from keras.preprocessing import sequence
    from keras.datasets import imdb

    max_features = 5000
    maxlen = 105

    (X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=max_features)
    X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
    X_test = sequence.pad_sequences(X_test, maxlen=maxlen)

    return {
        'train': {
            'in': {
                'headline-input': X_train[:, :100],
                'aux-input': X_train[:, -5 :],
            },

            'out': {
                'headline-output': y_train,
                'aux-output': y_train,
            },
        },

        'test': {
            'in': {
                'headline-input': X_test[:, :100],
                'aux-input': X_test[:, -5 :],
            },

            'out': {
                'headline-output': y_test,
                'aux-output': y_test,
            },
        },
    }



from pyspark import SparkContext, SparkConf

from picard.model_building.build import build_model
from picard.search.minimizer import Minimizer
from picard.search.spark_model import SparkMinimizer

conf = SparkConf().setAppName('decleras-test')
context = SparkContext(conf=conf)

sparkModel = SparkMinimizer(context)

minModel = sparkModel.minimize(
    space=hyperspec,
    data=get_data(),
    min_config={
        'max_evals': 1
    }
)

print(minModel)
