from math import floor
from pandas import read_csv
from ..preprocessors.by_type import preprocessors_by_type


# TODO: expose this config to something
split = 0.3

def get_picard_input(data_spec, path, hypermodel):

    fields_data = get_fields_data(
        data_spec['fields'],
        get_fields_df(data_spec['fields'], path)
    )

    num_rows = fields_data.items()[0][1].size
    split_idx = floor(num_rows * split)

    return {

        'train': {
            'in': dict([
                (
                    'input-{}'.format(fields_data[field_key]['idx']),
                    fields_data[field_key]['data'][split_idx:]
                )
                for field_key in data_spec['in']
            ]),
            'out': dict([
                (
                    'output-{}'.format(fields_data[field_key]['idx']),
                    fields_data[field_key]['data'][split_idx:]
                )
                for field_key in data_spec['out']
            ]),
        },

        'test': {
            'in': dict([
                (
                    'input-{}'.format(fields_data[field_key]['idx']),
                    fields_data[field_key]['data'][:split_idx]
                )
                for field_key in data_spec['in']
            ]),
            'out': dict([
                (
                    'output-{}'.format(fields_data[field_key]['idx']),
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
            {
                'idx': field_spec['idx'],
                'data': preprocessors_by_type[
                    field_spec['type']
                ](df[field_key])
            }
        )
        for (field_key, field_spec) in fields_spec.items()
    ])

def get_fields_df(fields_spec, path):
    field_keys = fields_spec.keys()

    return read_csv(path).dropna(
        subset=field_keys
    )[field_keys].reset_index(drop=True)

