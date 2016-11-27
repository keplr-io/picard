from .dates import process_date
from .floats import process_float
from .text_seqs import process_text_seq

'''

    A valid processor is a map

        pandas DataFrame -> numpy array


'''

preprocessors_by_type = {
    'date': process_date,
    'float': process_float,
    'text_seq': process_text_seq
}
