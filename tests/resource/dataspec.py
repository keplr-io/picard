dataspec = {
    'fields': {
        'title': {
            'type': 'text_seq',
            'shape': (500,)
        },
        'score': {
            'type': 'float',
            'shape': (1,)
        }
    },
    'in': [
        {
            'field': 'title',
            'leg': 'input'
        },
    ],
    'out': [
        {
            'field': 'score',
            'leg': 'output'
        }
    ],
    'training': {
        'split': 0.3,
        'val_split': 0.2,
        'epochs': 1
    }
}
