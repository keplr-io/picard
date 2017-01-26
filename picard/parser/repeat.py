'''
    Reduce #repeat specs to #compose specs
'''

def parse_repeat(spec):

    if isinstance(spec, dict):
        return dict([
            (key, parse_repeat(val))
            if key != '#repeat'
            else get_reduced_spec(val)
            for key, val in spec.items()
        ])

    if isinstance(spec, list):
        return [
            parse_repeat(item) for item in spec
        ]

    return spec

def get_reduced_spec(body):
    return (
        '#compose',
        [body['operator']] * body['times']
    )
