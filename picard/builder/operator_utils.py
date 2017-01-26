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

def get_next_state(operator_config, target_name, previous_state, parent_idx=0):

    if '#compose' in operator_config:
        ops = operator_config['#compose']

        return reduce(
            lambda state_data, op: get_next_state(
                op,
                state_data['target'][1:],
                state_data['state'],
                state_data['idx']
            ),
            ops,
            {
                'state': previous_state,
                'target': str(parent_idx) * len(ops) + '#' + str(parent_idx) + target_name,
                'idx': 0
            }
        )

    return {
        'state': get_operator(
            operator_config['layer'],
            operator_config['config'],
            target_name
        )(previous_state),
        'target': target_name,
        'idx': parent_idx + 1,
    }

def get_operator(name, spec, operator_name):

    '''
    Produces a Keras layer with given spec.
    '''

    return getattr(
        import_module('keras.layers'),
        name
    )(name=get_clean_op_name(operator_name), **spec)

def get_clean_op_name(op_name):
    if op_name[0] == '#':
        return op_name[2:].replace('#', '___')
    return op_name.replace('#', '___')