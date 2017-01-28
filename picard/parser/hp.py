from hyperopt import hp

def parse_hp(obj, obj_id='obj'):
    if isinstance(obj, dict):
        return parse_dict(obj, obj_id)

    if isinstance(obj, list):
        return parse_list(obj, obj_id)

    return obj

def parse_list(obj, obj_id):

    return [
        parse_hp(
            item,
            obj_id + '_' + str(idx)
        )
        for (idx, item) in enumerate(obj)
    ]

def parse_dict(obj, obj_id):

    if len(obj.items()) == 1:

        child_key = obj.keys()[0]
        if child_key[0] == '&':
            return apply_hp(
                obj_id, obj, child_key[1:]
            )

    return {
        key: parse_hp(value, obj_id + '_' + str(key))
        for (key, value) in obj.items()
    }

def apply_hp(obj_id, obj, cmd):

    return getattr(hp, cmd)(
        obj_id,
        **parse_hp(
            obj['&' + cmd],
            '{}__&{}'.format(obj_id, cmd)
        )
    )

