from importlib import import_module

def get_operator_image(previous_state, operator_key, target_key, operator_config):
    '''
    Given dict of precomputed operator composition results,
    '''

    if operator_key == 'IDENTITY':
        return previous_state

    return get_next_state(
        operator_config[operator_key],
        target_key,
        previous_state
    )['state']

def get_next_state(operator_config, target_name, previous_state):

    if '#compose' in operator_config:
        return reduce(
            lambda state_data, op: get_next_state(op, state_data['target'], state_data['state']),
            operator_config['#compose'],
            {
                'state': previous_state,
                'target': target_name
            }
        )
    print '======='
    print operator_config
    print '----'
    print previous_state
    print '...'
    return {
        'state': get_operator(
            operator_config['layer'],
            operator_config['config'],
            target_name + '_' + operator_config['layer']
        )(previous_state),
        'target': target_name + '_' + operator_config['layer']
    }

def get_operator(name, spec, operator_name):

    '''
    Produces a Keras layer with given spec.
    '''

    return getattr(
        import_module('keras.layers'),
        name
    )(name=operator_name, **spec)
