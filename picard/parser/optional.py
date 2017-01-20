'''
    Reduce #repeat specs to #compose specs
'''

def parse_optional(spec):

    if isinstance(spec, dict):
        return dict([
            (key, parse_optional(val))
            if not isinstance(val, list)
            else get_reduced_list(key, val)
            for key, val in spec.items()
        ])

    if isinstance(spec, list):
        return [
            parse_optional(item) for item in spec
        ]

    return spec

def get_reduced_list(key, ls):
    if has_optional_items(ls):
        return (
            '&choice',
            {
                'options': get_possible_lists(ls)
            }
        )
    return (key, parse_optional(ls))


def has_optional_items(ls):
    if not isinstance(ls, list):
        return False

    for item in ls:
        if is_optional(item):
            return True
    return False

def get_possible_lists(ls, head=0):
    if head >= len(ls):
        return [ls]

    if not is_optional(ls[head]):
        return get_possible_lists(ls, head + 1)

    rmls = ls[:head] + ls[head + 1:]
    return get_possible_lists(
        ls, head + 1
    ) + get_possible_lists(
        rmls, head
    )

def is_optional(item):
    return isinstance(item, dict) and '#optional' in item


def get_reduced_spec(body):
    return (
        '#compose',
        {
            'operators': [body['operator']] * body['times']
        }
    )
