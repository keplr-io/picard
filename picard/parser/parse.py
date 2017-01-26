from __future__ import absolute_import

from .inversion import parse_inversion
from .repeat import parse_repeat
from .optional import parse_optional
from .hp import parse_hp

def parse(spec):
    return parse_hp(
        preparse(spec)
    )

# parse without adding hyperopt objects
def preparse(spec):
    return parse_optional(
        parse_repeat(
            parse_inversion(spec)
        )
    )
