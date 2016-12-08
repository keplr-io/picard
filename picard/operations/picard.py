def apply_picard_operation(obj_id, obj, cmd, parse_config):
    cmd_body = obj['@' + cmd]

    if cmd == 'repeat':
        options = [
            [
                parse_config(
                    cmd_body['body'],
                    obj_id + '.x' + str(num_times)
                )
            ] * num_times

            for num_times in range(
                cmd_body['times'][0],
                cmd_body['times'][1] + 1
            )
        ]
        return hp.choice(obj_id + '.@repeat', options)

    if cmd == 'concat':
        parsed_body = parse_config(cmd_body, obj_id + '.@concat')

        if all([isinstance(child, list) for child in parsed_body]):
            return sum(parsed_body)

        return {
            '@concat': parsed_body
        }
