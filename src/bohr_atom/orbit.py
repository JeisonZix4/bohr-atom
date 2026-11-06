"""Cálculos de radios y cinemática orbital del modelo de Bohr.

Las magnitudes se refieren a la coordenada relativa electrón-núcleo,
consistente con el uso de la masa reducida en el problema de dos cuerpos.
"""

from math import pi

from .constants import (
    ELEMENTARY_CHARGE_C,
    REDUCED_PLANCK_CONSTANT_J_S,
    VACUUM_PERMITTIVITY_F_M,
)
from .validation import validate_positive_integer, validate_positive_real

# Factor de conversión expresado como cantidad de metros por unidad.
RADIUS_UNITS: dict[str, float] = {
    "m": 1.0,
    "nm": 1e-9,
    "pm": 1e-12,
    "angstrom": 1e-10,
}


def orbital_radius_m(
    n: int,
    Z: int,
    mu: float,
    elementary_charge_c: float = ELEMENTARY_CHARGE_C,
    epsilon_0: float = VACUUM_PERMITTIVITY_F_M,
    hbar: float = REDUCED_PLANCK_CONSTANT_J_S,
) -> float:
    """Calcula la separación electrón-núcleo de la órbita ``n``, en metros.

    La expresión se obtiene al combinar la fuerza de Coulomb con la
    cuantización del momento angular ``mu * v * r = n * hbar``.

    Parameters
    ----------
    n:
        Número cuántico principal, entero positivo.
    Z:
        Número atómico, entero positivo.
    mu:
        Masa reducida del sistema en kilogramos.
    elementary_charge_c:
        Magnitud de la carga elemental en culombios.
    epsilon_0:
        Permitividad eléctrica del vacío en faradios por metro.
    hbar:
        Constante de Planck reducida en julios-segundo.

    Returns
    -------
    float
        Distancia relativa electrón-núcleo en metros.
    """
    n = validate_positive_integer(n, "n")
    Z = validate_positive_integer(Z, "Z")
    mu = validate_positive_real(mu, "mu")
    charge = validate_positive_real(abs(elementary_charge_c), "elementary_charge_c")
    epsilon_0 = validate_positive_real(epsilon_0, "epsilon_0")
    hbar = validate_positive_real(hbar, "hbar")

    numerator = 4.0 * pi * epsilon_0 * hbar**2 * n**2
    denominator = mu * charge**2 * Z
    return numerator / denominator


def convert_radius(radius_m: float, unit: str = "m") -> float:
    """Convierte un radio en metros a una unidad admitida.

    Parameters
    ----------
    radius_m:
        Radio positivo expresado en metros.
    unit:
        Unidad de salida: ``'m'``, ``'nm'``, ``'pm'`` o ``'angstrom'``.

    Returns
    -------
    float
        Radio convertido a la unidad solicitada.

    Raises
    ------
    TypeError
        Si ``unit`` no es una cadena.
    ValueError
        Si la unidad no está admitida.
    """
    if not isinstance(unit, str):
        raise TypeError("unit debe ser una cadena de texto.")
    normalized_unit = unit.lower()
    if normalized_unit not in RADIUS_UNITS:
        raise ValueError(f"Unidad de radio no soportada: {unit}")

    radius_m = validate_positive_real(radius_m, "radius_m")
    return radius_m / RADIUS_UNITS[normalized_unit]


def orbital_angular_frequency_rad_s(
    n: int,
    Z: int,
    mu: float,
    elementary_charge_c: float = ELEMENTARY_CHARGE_C,
    epsilon_0: float = VACUUM_PERMITTIVITY_F_M,
    hbar: float = REDUCED_PLANCK_CONSTANT_J_S,
) -> float:
    """Calcula la velocidad angular orbital relativa en radianes/segundo.

    Se obtiene al combinar la ecuación de la fuerza centrípeta de Coulomb
    con la cuantización del momento angular. No es la frecuencia del fotón
    emitido o absorbido en una transición entre niveles.

    Parameters
    ----------
    n:
        Número cuántico principal.
    Z:
        Número atómico.
    mu:
        Masa reducida en kilogramos.
    elementary_charge_c:
        Magnitud de la carga elemental en culombios.
    epsilon_0:
        Permitividad del vacío en faradios por metro.
    hbar:
        Constante de Planck reducida en julios-segundo.

    Returns
    -------
    float
        Velocidad angular relativa en rad/s.
    """
    n = validate_positive_integer(n, "n")
    Z = validate_positive_integer(Z, "Z")
    mu = validate_positive_real(mu, "mu")
    charge = validate_positive_real(abs(elementary_charge_c), "elementary_charge_c")
    epsilon_0 = validate_positive_real(epsilon_0, "epsilon_0")
    hbar = validate_positive_real(hbar, "hbar")

    numerator = mu * Z**2 * charge**4
    denominator = (4.0 * pi * epsilon_0) ** 2 * hbar**3 * n**3
    return numerator / denominator


def orbital_period_s(angular_frequency_rad_s: float) -> float:
    """Calcula el período orbital a partir de una velocidad angular.

    Parameters
    ----------
    angular_frequency_rad_s:
        Velocidad angular positiva en radianes por segundo.

    Returns
    -------
    float
        Período orbital en segundos, ``2 pi / omega``.
    """
    omega = validate_positive_real(angular_frequency_rad_s, "angular_frequency_rad_s")
    return 2.0 * pi / omega
