import sys
import io

HEADER = "rprod:"
_VERBOSITY: int = 0


def set_verbosity(verbosity: int) -> None:
    """Set verbosity to -1 (quiet), 0 (default), 1, 2 or 3"""
    global _VERBOSITY
    if verbosity not in (-1, 0, 1, 2, 3):
        raise ValueError(verbosity)
    _VERBOSITY = verbosity


def message(verbosity: int, *args) -> None:
    """Print a message conditionally.
    The current verbosity must be greater than or equal to the verbosity argument
    If the current verbosity is at least two levels greater, wrap it in stars"""
    if _VERBOSITY >= verbosity:
        if _VERBOSITY >= verbosity + 2:
            f = io.StringIO()
            print(*args, file=f)
            msg = f.getvalue()
            print(HEADER, "*" * 60, file=sys.stderr)
            for l in msg.splitlines():
                print(HEADER, "*", l, file=sys.stderr)
            print(HEADER, "*" * 60, file=sys.stderr)
        else:
            print(HEADER, *args, file=sys.stderr)
