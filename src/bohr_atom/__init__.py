"""Biblioteca de cálculos para el modelo atómico de Bohr.

El punto de entrada público es :class:`BohrAtom`. Las constantes físicas
más utilizadas también se exportan para facilitar la creación de sistemas.
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
    "BOHR_RADIUS_M",
    "ELECTRON_MASS_KG",
    "ELEMENTARY_CHARGE_C",
    "HELIUM4_NUCLEUS_MASS_KG",
    "PROTON_MASS_KG",
    "RYDBERG_ENERGY_EV",
]
