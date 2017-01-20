data_spec = {
    'fields': {
        'title': {
            'type': 'text_seq',
            'shape': (500,)
        },
        'time_ts': {
            'type': 'date',
            'shape': (1,)
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
    ]
}
