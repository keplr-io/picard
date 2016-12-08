spec = {

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
                'activation': 'relu'
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
            'input-0': {
                'dtype': 'int32'
            },

            'input-1': {
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

        'edges': {
            '@concat': [
                [
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
                        'source': 'post-dense2',
                        'target': 'post-dense3',
                        'operator': 'dense'
                    },

                    {
                        'source': 'post-dense3',
                        'target': 'output-0',
                        'operator': 'smallDense'
                    }
                ],
                {
                    '#compose': {
                        'source': 'pre-dense',
                        'target': 'post-dense1',
                        'operators': [
                            'dense',
                            'dense',
                            'dense'
                        ]
                    }
                }#,
                # {
                #     '#repeat': {
                #         'source': 'post-dense1',
                #         'target': 'post-dense2',
                #         'operator': 'dense',
                #         'times': 3
                #     }
                # }
            ]
        }

    },

    'compile': {
        'optimizer': 'rmsprop'
    },

    'fit': {
        'batch_size': 64,
    }
}
