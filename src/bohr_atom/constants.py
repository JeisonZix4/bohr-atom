"""Constantes físicas utilizadas por la biblioteca ``bohr_atom``.

Los valores están expresados en unidades del Sistema Internacional (SI),
salvo las constantes cuyo nombre indica explícitamente otra unidad.
Las masas nucleares de referencia corresponden al protón y al núcleo de
helio-4; no deben confundirse con las masas atómicas de átomos neutros.
"""

from math import pi

# Constantes fundamentales: valores recomendados de CODATA 2022.
ELEMENTARY_CHARGE_C: float = 1.602176634e-19
ELECTRON_MASS_KG: float = 9.1093837139e-31
PROTON_MASS_KG: float = 1.67262192595e-27
HELIUM4_NUCLEUS_MASS_KG: float = 6.6446573450e-27
VACUUM_PERMITTIVITY_F_M: float = 8.8541878188e-12
PLANCK_CONSTANT_J_S: float = 6.62607015e-34
REDUCED_PLANCK_CONSTANT_J_S: float = PLANCK_CONSTANT_J_S / (2.0 * pi)
SPEED_OF_LIGHT_M_S: float = 299792458.0

# Un electronvoltio es la energía que adquiere una carga elemental al
# atravesar una diferencia de potencial de un voltio.
ELECTRONVOLT_J: float = ELEMENTARY_CHARGE_C

# Radio de Bohr y energía de Rydberg para un núcleo de masa infinita.
BOHR_RADIUS_M: float = (
    4.0
    * pi
    * VACUUM_PERMITTIVITY_F_M
    * REDUCED_PLANCK_CONSTANT_J_S**2
    / (ELECTRON_MASS_KG * ELEMENTARY_CHARGE_C**2)
)

RYDBERG_ENERGY_EV: float = (
    ELECTRON_MASS_KG
    * ELEMENTARY_CHARGE_C**4
    / (
        2.0
        * (4.0 * pi * VACUUM_PERMITTIVITY_F_M) ** 2
        * REDUCED_PLANCK_CONSTANT_J_S**2
        * ELECTRONVOLT_J
    )
)
