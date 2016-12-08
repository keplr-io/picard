data_spec = {
    'fields': {
        'title': {
            'type': 'text_seq',
            'shape': (1000,)
        },
        'time_ts': {
            'type': 'date',
            'shape': (5,)
        },
        'score': {
            'type': 'float',
            'shape': (1,)
        }
    },
    'in': [
        {
            'field': 'title',
            'leg': 'input-0'
        },
        {
            'field': 'time_ts',
            'leg': 'input-1'
        }
    ],
    'out': [
        {
            'field': 'score',
            'leg': 'output-0'
        }
    ]
}
