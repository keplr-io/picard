from hyperopt import hp

def apply_hyperopt_operation(obj_id, obj, cmd, parse_config):

    return getattr(hp, cmd)(
        obj_id,
        **parse_config(
            obj['&' + cmd],
            '{}.&{}'.format(obj_id, cmd)
        )
    )
