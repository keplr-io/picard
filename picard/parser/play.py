from parse import parse

print parse({
    'operators': {
        'ff': {
            '#repeat': {
                '+times': {
                    '&randint': {
                        'upper': 5
                    }
                },
                'operator': {
                    '#compose': {
                        'operators': [
                            {
                                'layer': 'Dense',
                                'output_dim': 64,
                                'activation': {
                                    '&choice': {
                                        'options': ['relu', 'sigmoid']
                                    }
                                }
                            },
                            {
                                '#optional': {
                                    'layer': 'Dropout',
                                    'p': {
                                        '&uniform': {
                                            'low': 0,
                                            'high': .5
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        },
        'denseOut': {}
    },
    'graph': {
        'legs': {
            'in': ['input'],
            'out': ['output']
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
        ]
    }
})
