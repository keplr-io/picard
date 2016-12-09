
def apply_graph_operation(obj_id, obj, cmd, parse_config):

    if cmd == 'compose':
        config = parse_config(obj['#compose'])
        return get_composed_spec(
            obj_id,
            config['source'],
            config['target'],
            config['operators']
        )

    if cmd == 'repeat':
        config = parse_config(obj['#repeat'])
        # print([config['operator']] * config['times'])
        return get_composed_spec(
            obj_id,
            config['source'],
            config['target'],
            [config['operator']] * config['times']
        )

def get_composed_spec(obj_id, source, target, operators):
    return [

        {
            'source': source,
            'target': get_middle_node(obj_id, operators[0], 0),
            'operator': operators[0]
        }

    ] + [

        {
            'source': get_middle_node(obj_id, operators[idx], idx),
            'target': get_middle_node(obj_id, operator, idx + 1),
            'operator': operator
        }

        for idx, operator in enumerate(operators[1:-1])

    ] + [

        {
            'source': get_middle_node(
                obj_id, operators[-2], len(operators) - 2
            ),
            'target': target,
            'operator': operators[-1]
        }

    ]

def get_middle_node(obj_id, operator, idx):
    return 'compose-layer-{}-{}-{}'.format(
        obj_id.replace('@','PICARD-'), operator, idx
    )
