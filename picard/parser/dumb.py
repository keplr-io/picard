print dict([('#compose', [{
        '#compose': [{
            'layer': 'Dense',
            'config': {
                'output_dim': 64,
                'activation': {
                    '&choice': {
                        'options': ['relu', 'sigmoid']
                    }
                }
            }
        }, {
            '#optional': {
                'layer': 'Dropout',
                'config': {
                    'p': {
                        '&uniform': {
                            'high': 0.5,
                            'low': 0
                        }
                    }
                }
            }
        }]
    }, {
        '#compose': [{
            'layer': 'Dense',
            'config': {
                'output_dim': 64,
                'activation': {
                    '&choice': {
                        'options': ['relu', 'sigmoid']
                    }
                }
            }
        }, {
            '#optional': {
                'layer': 'Dropout',
                'config': {
                    'p': {
                        '&uniform': {
                            'high': 0.5,
                            'low': 0
                        }
                    }
                }
            }
        }]
    }
])])
