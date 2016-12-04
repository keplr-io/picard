from math import floor
from pandas import read_csv
from ..preprocessors.by_type import preprocessors_by_type


# TODO: expose this config to something
split = 0.3

def get_picard_input(data_spec, path):

    fields_spec = data_spec['fields']

    fields_data = get_fields_data(
        fields_spec,
        get_fields_df(fields_spec, path)
    )

    split_idx = floor(fields_data.items()[0][1].size * split)

    def get_input_key(field_key):
        return 'input-{}'.format(fields_spec[field_key]['idx'])

    def get_output_key(field_key):
        return 'output-{}'.format(fields_spec[field_key]['idx'])

    return {

        'train': {
            'in': dict([
                (
                    get_input_key(field_key),
                    fields_data[field_key]['data'][split_idx:]
                )
                for field_key in data_spec['in']
            ]),
            'out': dict([
                (
                    get_output_key(field_key),
                    fields_data[field_key]['data'][split_idx:]
                )
                for field_key in data_spec['out']
            ]),
        },

        'test': {
            'in': dict([
                (
                    get_input_key(field_key),
                    fields_data[field_key]['data'][:split_idx]
                )
                for field_key in data_spec['in']
            ]),
            'out': dict([
                (
                    get_output_key(field_key),
                    fields_data[field_key]['data'][:split_idx]
                )
                for field_key in data_spec['out']
            ]),
        },

    }

def get_fields_data(fields_spec, df):
    return dict([
        (
            field_key,
            preprocessors_by_type[
                field_spec['type']
            ](df[field_key])
        )
        for (field_key, field_spec) in fields_spec.items()
    ])

def get_fields_df(fields_spec, path):
    field_keys = fields_spec.keys()

    return read_csv(path).dropna(
        subset=field_keys
    )[field_keys].reset_index(drop=True)

