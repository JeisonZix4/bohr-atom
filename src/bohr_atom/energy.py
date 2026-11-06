"""Cálculos energéticos del modelo de Bohr para sistemas hidrogenoides.

El problema de dos cuerpos electrón-núcleo se reduce al movimiento relativo
utilizando la masa reducida. La energía calculada corresponde a la energía
de enlace respecto al límite de ionización, tomado como energía cero.
"""

from math import pi

from .constants import (
    ELEMENTARY_CHARGE_C,
    REDUCED_PLANCK_CONSTANT_J_S,
    VACUUM_PERMITTIVITY_F_M,
)
from .validation import validate_positive_integer, validate_positive_real


def reduced_mass(electron_mass_kg: float, nucleus_mass_kg: float) -> float:
    """Calcula la masa reducida del sistema electrón-núcleo.

    La masa reducida permite describir el movimiento relativo de dos cuerpos
    mediante un problema equivalente de una sola partícula.

    Parameters
    ----------
    electron_mass_kg:
        Masa del electrón en kilogramos.
    nucleus_mass_kg:
        Masa del núcleo en kilogramos.

    Returns
    -------
    float
        Masa reducida en kilogramos: ``m_e M / (m_e + M)``.
    """
    electron_mass = validate_positive_real(electron_mass_kg, "electron_mass_kg")
    nucleus_mass = validate_positive_real(nucleus_mass_kg, "nucleus_mass_kg")
    return electron_mass * nucleus_mass / (electron_mass + nucleus_mass)


def energy_level_joule(
    n: int,
    Z: int,
    mu: float,
    elementary_charge_c: float = ELEMENTARY_CHARGE_C,
    epsilon_0: float = VACUUM_PERMITTIVITY_F_M,
    hbar: float = REDUCED_PLANCK_CONSTANT_J_S,
) -> float:
    """Calcula la energía del nivel ``n`` en julios.

    Se implementa la expresión de Bohr con masa reducida:

    ``E_n = -mu Z² e⁴ / [2 (4 pi epsilon_0)² hbar² n²]``.

    Parameters
    ----------
    n:
        Número cuántico principal, entero positivo.
    Z:
        Número atómico, entero positivo.
    mu:
        Masa reducida electrón-núcleo en kilogramos.
    elementary_charge_c:
        Magnitud de la carga elemental en culombios. Se usa el valor
        absoluto porque la energía depende de ``e⁴``.
    epsilon_0:
        Permitividad eléctrica del vacío en faradios por metro.
    hbar:
        Constante de Planck reducida en julios-segundo.

    Returns
    -------
    float
        Energía del estado ligado en julios. El signo negativo indica
        que el electrón está ligado al núcleo.
    """
    n = validate_positive_integer(n, "n")
    Z = validate_positive_integer(Z, "Z")
    mu = validate_positive_real(mu, "mu")
    charge = validate_positive_real(abs(elementary_charge_c), "elementary_charge_c")
    epsilon_0 = validate_positive_real(epsilon_0, "epsilon_0")
    hbar = validate_positive_real(hbar, "hbar")

    numerator = mu * Z**2 * charge**4
    denominator = 2.0 * (4.0 * pi * epsilon_0) ** 2 * hbar**2 * n**2
    return -numerator / denominator
