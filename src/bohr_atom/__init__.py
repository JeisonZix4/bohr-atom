"""
Bohr Atom package.
"""

from .atom import BohrAtom
from .constants import (
    BOHR_RADIUS_M,
    ELECTRON_MASS_KG,
    ELEMENTARY_CHARGE_C,
    HELIUM4_NUCLEUS_MASS_KG,
    PROTON_MASS_KG,
    RYDBERG_ENERGY_EV,
)

__version__ = "0.1.0"

__all__ = [
    "BohrAtom",
    "ELEMENTARY_CHARGE_C",
    "ELECTRON_MASS_KG",
    "PROTON_MASS_KG",
    "HELIUM4_NUCLEUS_MASS_KG",
    "BOHR_RADIUS_M",
    "RYDBERG_ENERGY_EV",
]
