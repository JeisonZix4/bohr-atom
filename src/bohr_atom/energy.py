"""
Energy calculations for hydrogen-like atoms.
"""

from math import pi

from .constants import (
    ELEMENTARY_CHARGE_C,
    REDUCED_PLANCK_CONSTANT_J_S,
    VACUUM_PERMITTIVITY_F_M,
)
from .validation import validate_positive_integer, validate_positive_real


def reduced_mass(electron_mass_kg, nucleus_mass_kg):
    """
    Calculate the reduced mass of the electron-nucleus system.

    Parameters
    ----------
    electron_mass_kg : float
        Electron mass in kg.

    nucleus_mass_kg : float
        Nuclear mass in kg.

    Returns
    -------
    float
        Reduced mass in kg.
    """

    me = validate_positive_real(electron_mass_kg, "electron_mass_kg")

    M = validate_positive_real(nucleus_mass_kg, "nucleus_mass_kg")

    return (me * M) / (me + M)


def energy_level_joule(
    n,
    Z,
    mu,
    elementary_charge_c=ELEMENTARY_CHARGE_C,
    epsilon_0=VACUUM_PERMITTIVITY_F_M,
    hbar=REDUCED_PLANCK_CONSTANT_J_S,
):
    """
    Calculate the Bohr energy level in joules.
    """

    n = validate_positive_integer(n, "n")

    Z = validate_positive_integer(Z, "Z")

    mu = validate_positive_real(mu, "reduced_mass")

    charge = validate_positive_real(abs(elementary_charge_c), "elementary_charge")

    epsilon_0 = validate_positive_real(epsilon_0, "epsilon_0")

    hbar = validate_positive_real(hbar, "hbar")

    numerator = mu * Z**2 * charge**4

    denominator = 2 * (4 * pi * epsilon_0) ** 2 * hbar**2 * n**2

    return -numerator / denominator
