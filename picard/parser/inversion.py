'''
    Occasionally a hyperopt operator with a discrete RHS
    can change the number of parameters. In Picard this is explicitly declared
    by an '+' in the property key whose RHS is a hyperopt operator.

    TODO: come up with a better fucking name for this
'''
def parse_inversion(spec):

    if isinstance(spec, dict):
        return dict([
            (key, parse_inversion(val))
            if get_inversion_spec_key(val) is None
            else get_inverted_spec(key, val)
            for key, val in spec.items()
        ])

    if isinstance(spec, list):
        return [
            parse_inversion(item) for item in spec
        ]

    return spec

def get_inverted_spec(key, body):
    inv_spec_key = get_inversion_spec_key(body)
    inv_spec_val = body[inv_spec_key]
    return (
        '&choice',
        {
            'options': get_inv_options(
                key, body, inv_spec_key, inv_spec_val
            )
        }
    )

def get_inv_options(key, body, inv_spec_key, inv_spec_val):
    hp_spec_key = get_hp_spec_key(inv_spec_val)
    hp_spec_body = inv_spec_val[hp_spec_key]

    if hp_spec_key == '&randint':
        return [
            get_choice_option(k, key, body, inv_spec_key)
            for k in range(1, hp_spec_body['upper'])
        ]

    if hp_spec_key == '&choice':
        return [
            get_choice_option(option, key, body, inv_spec_key)
            for option in hp_spec_body['options']
        ]

def get_choice_option(option, key, body, inv_spec_key):
    return {
        key: get_dict_excluding_keys(
            get_merged_dicts(body, {
                inv_spec_key[1:]: option
            }),
            [inv_spec_key]
        )
    }

def get_hp_spec_key(obj):
    return get_spec_key('&', obj)

def get_inversion_spec_key(obj):
    return get_spec_key('+', obj)

def get_spec_key(symbol, obj):

    if isinstance(obj, dict):
        for key, val in obj.items():
            if key[0] == symbol:
                return key
    return None

def get_merged_dicts(a, b):
    a.copy()
    a.update(b)
    return a

def get_dict_excluding_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}
