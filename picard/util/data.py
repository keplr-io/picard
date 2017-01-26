from math import floor

def get_picard_input(data_spec, fields_data):
    split = data_spec['training']['split']
    split_idx = int(floor(len(fields_data.items()[0][1]) * split))

    return {

        'train': {
            'in': dict([
                (
                    field_spec['leg'],
                    fields_data[field_spec['field']][split_idx:]
                )
                for field_spec in data_spec['in']
            ]),
            'out': dict([
                (
                    field_spec['leg'],
                    fields_data[field_spec['field']][split_idx:]
                )
                for field_spec in data_spec['out']
            ]),
        },

        'test': {
            'in': dict([
                (
                    field_spec['leg'],
                    fields_data[field_spec['field']][:split_idx]
                )
                for field_spec in data_spec['in']
            ]),
            'out': dict([
                (
                    field_spec['leg'],
                    fields_data[field_spec['field']][:split_idx]
            )
                for field_spec in data_spec['out']
            ]),
        },

    }
