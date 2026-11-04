"""
Physical constants used in the Bohr atomic model.

Values are expressed in SI units.
"""

import math

# Fundamental constants

ELEMENTARY_CHARGE_C = 1.602176634e-19

ELECTRON_MASS_KG = 9.1093837139e-31

PROTON_MASS_KG = 1.67262192595e-27

HELIUM4_NUCLEUS_MASS_KG = 6.6446573450e-27


VACUUM_PERMITTIVITY_F_M = 8.8541878188e-12

PLANCK_CONSTANT_J_S = 6.62607015e-34

REDUCED_PLANCK_CONSTANT_J_S = PLANCK_CONSTANT_J_S / (2 * math.pi)

SPEED_OF_LIGHT_M_S = 299792458


# Derived constants

ELECTRONVOLT_J = ELEMENTARY_CHARGE_C

BOHR_RADIUS_M = (
    4
    * math.pi
    * VACUUM_PERMITTIVITY_F_M
    * REDUCED_PLANCK_CONSTANT_J_S**2
    / (ELECTRON_MASS_KG * ELEMENTARY_CHARGE_C**2)
)


# Reference energy for an infinitely massive nucleus

RYDBERG_ENERGY_EV = (
    ELECTRON_MASS_KG
    * ELEMENTARY_CHARGE_C**4
    / (
        2
        * (4 * math.pi * VACUUM_PERMITTIVITY_F_M) ** 2
        * REDUCED_PLANCK_CONSTANT_J_S**2
        * ELECTRONVOLT_J
    )
)
