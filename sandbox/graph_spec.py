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
            'headline-input': {
                'shape': (100, ),
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
        'optimizer': 'rmsprop'
    },

}
