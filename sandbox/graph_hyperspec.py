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
            'input-1': {
                'dtype': 'int32'
            },

            'input-2': {
            }
        },

        'outgoing': {
            'output-0': {
                'loss': 'binary_crossentropy',
            },
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
                'source': 'input-0',
                'target': 'post-embedding',
                'operator': 'embedding'
            },
            {
                'source': 'post-embedding',
                'target': 'post-lstm',
                'operator': 'lstm'
            },
            {
                'source': 'input-1',
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
                'operator': {
                    '#compose': {
                        'operators': [
                            'dense',
                            'dense'
                        ]
                    }
                }
            },
            {
                'source': 'post-dense1',
                'target': 'post-dense2',
                'operator': {
                    '#repeat': {
                        'operator': 'dense',
                        'times': {
                            '$randint': 5
                        }
                    }
                }
            },
            {
                'source': 'post-dense2',
                'target': 'post-dense3',
                'operator': 'dense'
            },
            {
                'source': 'post-dense3',
                'target': 'output-0',
                'operator': 'smallDense'
            }
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
