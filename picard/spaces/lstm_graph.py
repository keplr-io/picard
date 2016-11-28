def get_space(data_spec):

    return {

        #TODO: correctly compute all the fields here

        'operators': {

            'embedding': {
                'operator': 'Embedding',

                'spec': {
                    'output_dim': 512,
                    'input_dim': 10000,
                    'input_length': 500
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
                #TODO: crrectly compute these fields

                'title': {
                    'shape': (500,),
                    'dtype': 'int32'
                },

                'time_ts': {
                    'shape': (1,)
                }

            },

            'outgoing': {

                'score': {
                    'loss': 'binary_crossentropy',
                    # 'loss_weight': 1.
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
                    'source': 'title',
                    'target': 'post-embedding',
                    'operator': 'embedding'
                },
                {
                    'source': 'post-embedding',
                    'target': 'post-lstm',
                    'operator': 'lstm'
                },
                {
                    'source': 'time_ts',
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
                    'target': 'score',
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
