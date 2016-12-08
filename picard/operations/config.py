from .hp import apply_hyperopt_operation
from .picard import apply_picard_operation
from .graph import apply_graph_operation

prefix_operation_map = {
    '&': apply_hyperopt_operation,
    '@': apply_picard_operation,
    '#': apply_graph_operation
}
