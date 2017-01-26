modelspec = {
    'operators': {
        'ff': {
            '#compose': ({
                '#compose': ({
                    'layer': 'Dense',
                    'config': {
                        'activation': 'relu',
                        'output_dim': 64
                    }
                }, {
                    'layer': 'Dropout',
                    'config': {
                        'p': 0.44874479157662
                    }
                })
            }, {
                '#compose': ({
                    'layer': 'Dense',
                    'config': {
                        'activation': 'sigmoid',
                        'output_dim': 64
                    }
                }, )
            }, {
                '#compose': ({
                    'layer': 'Dense',
                    'config': {
                        'activation': 'sigmoid',
                        'output_dim': 64
                    }
                }, {
                    'layer': 'Dropout',
                    'config': {
                        'p': 0.226596032739373
                    }
                })
            }, {
                '#compose': ({
                    'layer': 'Dense',
                    'config': {
                        'activation': 'sigmoid',
                        'output_dim': 64
                    }
                }, {
                    'layer': 'Dropout',
                    'config': {
                        'p': 0.4371277936356525
                    }
                })
            })
        },
        'denseOut': {
            'layer': 'Dense',
            'config': {
                'activation': 'sigmoid',
                'output_dim': 1
            }
        }
    },
    'legs': {
        'in': {
            'input': {}
        },
        'out': {
            'output': {
                'loss': 'binary_crossentropy'
            }
        }
    },
    'edges': ({
        'operator': 'IDENTITY',
        'source': 'input',
        'target': 'ffStart'
    }, {
        'operator': 'ff',
        'source': 'ffStart',
        'target': 'ffEnd'
    }, {
        'operator': 'denseOut',
        'source': 'ffEnd',
        'target': 'output'
    }),
    'compile': {
        'optimizer': 'rmsprop'
    },

    'fit': {
        'batch_size': {
            '&choice': 64
        },
    }

}
