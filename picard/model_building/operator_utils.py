from importlib import import_module

def get_operator_image(previous_state, operator_key, target_key, operator_spec):
    '''
    Given dict of precomputed operator composition results,
    '''

    if operator_key == 'IDENTITY':
        return previous_state

    operator_config = operator_spec[operator_key]

    return get_operator(
        operator_config['operator'],
        operator_config['spec'],
        target_key
    )(previous_state)


def get_operator(name, spec, operator_name):

    '''
    Produces a Keras layer with given spec.
    '''

    return getattr(
        import_module('keras.layers'),
        name
    )(name=operator_name, **spec)
