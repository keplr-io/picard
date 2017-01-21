spec = {
    'graph': {
        'legs': {
            'in': ('input', ),
            'out': ('output', )
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
        })
    },
    'operators': {
        'ff': {
            '#compose': {
                'operators': ({
                    '#compose': ({
                        'activation': 'sigmoid',
                        'layer': 'Dense',
                        'output_dim': 64
                    }, {
                        '#optional': {
                            'p': 0.48838714572798964,
                            'layer': 'Dropout'
                        }
                    })
                }, {
                    '#compose': ({
                        'activation': 'relu',
                        'layer': 'Dense',
                        'output_dim': 64
                    }, )
                })
            }
        },
        'denseOut': {}
    }
}