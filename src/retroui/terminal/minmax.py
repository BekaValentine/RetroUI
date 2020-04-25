from typing import TypeVar


T = TypeVar('T', int, float)


def minmax(n, lo, hi):
    # type: (T,T,T) -> T
    """
    Enforce that a number is within a range of numbers.
    """

    return max(lo, min(hi, n))
