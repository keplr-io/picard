from picard.util.data import get_picard_input

picard_input = get_picard_input(
    {
        'fields': {
            'title': {
                'type': 'text_seq'
            },
            'time_ts': {
                'type': 'date'
            },
            'score': {
                'type': 'float'
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
