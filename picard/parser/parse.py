from inversion import parse_inversion
from reduction import parse_repeat
from optional import parse_optional
from hp import parse_hp

def parse(spec):
    return parse_hp(
        parse_optional(
            parse_repeat(
                parse_inversion(spec)
            )
        )
    )
