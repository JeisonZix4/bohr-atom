"""
Input validation utilities.
"""

from math import isfinite
from numbers import Integral, Real


def validate_positive_integer(value, name="value"):

    if isinstance(value, bool) or not isinstance(value, Integral):
        raise TypeError(f"{name} must be an integer.")

    if value < 1:
        raise ValueError(f"{name} must be greater than or equal to 1.")

    return int(value)


def validate_positive_real(value, name="value"):

    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")

    value = float(value)

    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive.")

    return value
