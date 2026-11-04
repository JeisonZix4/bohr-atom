"""
Orbital radius calculations.
"""

from math import pi

from .constants import (
    ELEMENTARY_CHARGE_C,
    REDUCED_PLANCK_CONSTANT_J_S,
    VACUUM_PERMITTIVITY_F_M,
)
from .validation import validate_positive_integer, validate_positive_real

RADIUS_UNITS = {"m": 1.0, "nm": 1e-9, "pm": 1e-12, "angstrom": 1e-10}


def orbital_radius_m(
    n,
    Z,
    mu,
    elementary_charge_c=ELEMENTARY_CHARGE_C,
    epsilon_0=VACUUM_PERMITTIVITY_F_M,
    hbar=REDUCED_PLANCK_CONSTANT_J_S,
):
    """
    Calculate the electron-nucleus separation
    for a Bohr orbit, in meters.
    """

    n = validate_positive_integer(n, "n")

    Z = validate_positive_integer(Z, "Z")

    mu = validate_positive_real(mu, "reduced_mass")

    charge = validate_positive_real(abs(elementary_charge_c), "elementary_charge")

    epsilon_0 = validate_positive_real(epsilon_0, "epsilon_0")

    hbar = validate_positive_real(hbar, "hbar")

    numerator = 4 * pi * epsilon_0 * hbar**2 * n**2

    denominator = mu * charge**2 * Z

    return numerator / denominator


def convert_radius(radius_m, unit="m"):
    """
    Convert an orbital radius from meters
    to the requested unit.
    """

    unit = unit.lower()

    if unit not in RADIUS_UNITS:
        raise ValueError(f"Unsupported radius unit: {unit}")

    return radius_m / RADIUS_UNITS[unit]
