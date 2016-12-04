from picard.util.data import get_picard_input

picard_input = get_picard_input(
    {
        'fields': {
            'title': {
                'type': 'text_seq',
                'shape': (1000,)
            },
            'time_ts': {
                'type': 'date'
                'shape': (5,)
            },
            'score': {
                'type': 'float',
                'shape': (1,)
            }
        },
        'in': [
            'title',
            'time_ts'
        ],
        'out': [
            'score'
        ]
    },
    './sandbox/data/hn/0.csv'
)


print picard_input


print picard_input['train']['in']['title'].shape
