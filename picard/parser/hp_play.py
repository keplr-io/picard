from parse import parse

# define an objective function
def objective(args):
    print args
    return 1

from hyperopt import hp
from hyperopt import fmin, tpe

space = parse({
    'operators': {
        'ff': {
            '#repeat': {
                '+times': {
                    '&randint': {
                        'upper': 5
                    }
                },
                'operator': {
                    '#compose': [
                        {
                            'layer': 'Dense',
                            'config': {
                                'output_dim': 64,
                                'activation': {
                                    '&choice': {
                                        'options': ['relu', 'sigmoid']
                                    }
                                }
                            }
                        },
                        {
                            '#optional': {
                                'layer': 'Dropout',
                                'config': {
                                    'p': {
                                        '&uniform': {
                                            'low': 0,
                                            'high': .5
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        },
        'denseOut': {
            'layer': 'Dense',
            'config': {
                'output_dim': 5,
                'activation': {
                    '&choice': {
                        'options': ['relu', 'sigmoid']
                    }
                }
            }
        }
    },
    'legs': {
        'in': {'input': {}},
        'out': {'output': {}}
    },
    'edges': [
        {
            'source': 'input',
            'target': 'ffStart',
            'operator': 'IDENTITY'
        },
        {
            'source': 'ffStart',
            'target': 'ffEnd',
            'operator': 'ff'
        },
        {
            'source': 'ffEnd',
            'target': 'output',
            'operator': 'denseOut'
        }
    ],

    'compile': {
        'optimizer': {
            '&choice': {
                'options': ['rmsprop', 'adam']
            }
        }
    },

    'fit': {
        'batch_size': {
            '&choice': {
                'options': [64, 128]
            }
        },
    }

})

best = fmin(objective, space, algo=tpe.suggest, max_evals=10)

print best
