'''
    Utilities for parsing hyperparameter space configurations
'''

from operations.parser import get_parser, compose_parsers
parse_hyperspec = compose_parsers(
    get_parser(['@']),
    get_parser(['&'])
)

parse_hypermodel = compose_parsers(
    get_parser(['@']),
    get_parser(['#'])
)
