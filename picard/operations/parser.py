from .config import prefix_operation_map

def get_parser(allowed_prefixes):

    operations = dict([
        (prefix, operation)
        for (prefix, operation) in prefix_operation_map.items()
        if prefix in  allowed_prefixes
    ])

    def parse_config(obj, obj_id='obj'):
        if isinstance(obj, dict):
            return parse_dict(obj, obj_id)

        if isinstance(obj, list):
            return parse_list(obj, obj_id)

        return obj


    def parse_list(obj, obj_id):

        return [
            parse_config(
                item,
                obj_id + '.' + str(idx)
            )
            for (idx, item) in enumerate(obj)
        ]


    def parse_dict(obj, obj_id):

        if len(obj.items()) == 1:

            child_key = obj.keys()[0]

            if child_key[0] in operations:

                return operations[child_key[0]](
                    obj_id, obj, child_key[1:], parse_config
                )

        return {
            key: parse_config(value, obj_id + '.' + str(key))
            for (key, value) in obj.items()
        }

    return parse_config