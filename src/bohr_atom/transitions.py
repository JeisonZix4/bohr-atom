"""Cálculos de transiciones electrónicas y propiedades de fotones.

El signo de ``E_final - E_inicial`` determina si el átomo absorbe o emite
energía. La energía del fotón se reporta siempre como una magnitud positiva.
"""

from math import isfinite
from numbers import Real

from .constants import (
    ELEMENTARY_CHARGE_C,
    PLANCK_CONSTANT_J_S,
    SPEED_OF_LIGHT_M_S,
)
from .validation import validate_positive_integer, validate_positive_real


def transition_properties(
    n_initial: int,
    n_final: int,
    energy_initial_j: float,
    energy_final_j: float,
    h: float = PLANCK_CONSTANT_J_S,
    c: float = SPEED_OF_LIGHT_M_S,
    elementary_charge_c: float = ELEMENTARY_CHARGE_C,
) -> dict[str, float | int | str]:
    """Calcula las propiedades del fotón asociado a una transición.

    Parameters
    ----------
    n_initial, n_final:
        Números cuánticos principal inicial y final. Deben ser enteros
        positivos y diferentes.
    energy_initial_j, energy_final_j:
        Energías inicial y final del átomo en julios.
    h:
        Constante de Planck en J s.
    c:
        Velocidad de la luz en m/s.
    elementary_charge_c:
        Magnitud de la carga elemental en culombios, usada para convertir
        la energía del fotón a electronvoltios.

    Returns
    -------
    dict
        Diccionario con niveles, proceso, variación de energía del átomo,
        energía del fotón, frecuencia y longitud de onda.

    Notes
    -----
    Se utiliza ``delta_energy_atom_j = E_final - E_inicial``. Por tanto,
    una transición descendente tiene delta negativo y representa emisión.
    """
    n_initial = validate_positive_integer(n_initial, "n_initial")
    n_final = validate_positive_integer(n_final, "n_final")
    if n_initial == n_final:
        raise ValueError("Los niveles inicial y final deben ser diferentes.")

    for value, name in (
        (energy_initial_j, "energy_initial_j"),
        (energy_final_j, "energy_final_j"),
    ):
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError(f"{name} debe ser un número real.")
        if not isfinite(float(value)):
            raise ValueError(f"{name} debe ser finito.")

    h = validate_positive_real(h, "h")
    c = validate_positive_real(c, "c")
    elementary_charge_c = validate_positive_real(
        abs(elementary_charge_c), "elementary_charge_c"
    )

    delta_energy = float(energy_final_j) - float(energy_initial_j)
    photon_energy = abs(delta_energy)
    process = "emission" if delta_energy < 0.0 else "absorption"

    # La frecuencia se obtiene de E_gamma = h * nu y la longitud de onda
    # de lambda = c / nu. No se incluye aquí el retroceso del núcleo.
    frequency = photon_energy / h
    wavelength = c / frequency

    return {
        "initial_level": n_initial,
        "final_level": n_final,
        "process": process,
        "delta_energy_atom_j": delta_energy,
        "photon_energy_j": photon_energy,
        "photon_energy_ev": photon_energy / elementary_charge_c,
        "frequency_hz": frequency,
        "wavelength_m": wavelength,
        "wavelength_nm": wavelength * 1e9,
    }
