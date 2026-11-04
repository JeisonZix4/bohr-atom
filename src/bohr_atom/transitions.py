"""
Spectral transition calculations.
"""

from math import isfinite

from .constants import ELEMENTARY_CHARGE_C, PLANCK_CONSTANT_J_S, SPEED_OF_LIGHT_M_S
from .validation import validate_positive_integer


def transition_properties(
    n_initial,
    n_final,
    energy_initial_j,
    energy_final_j,
    h=PLANCK_CONSTANT_J_S,
    c=SPEED_OF_LIGHT_M_S,
    elementary_charge_c=ELEMENTARY_CHARGE_C,
):
    """
    Calculate photon properties for a transition.
    """

    n_initial = validate_positive_integer(n_initial, "n_initial")

    n_final = validate_positive_integer(n_final, "n_final")

    if n_initial == n_final:
        raise ValueError("Initial and final levels must be different.")

    if not isfinite(energy_initial_j):
        raise ValueError("Initial energy must be finite.")

    if not isfinite(energy_final_j):
        raise ValueError("Final energy must be finite.")

    delta_energy = energy_final_j - energy_initial_j

    photon_energy = abs(delta_energy)

    process = "emission" if delta_energy < 0 else "absorption"

    frequency = photon_energy / h

    wavelength = c / frequency

    photon_energy_ev = photon_energy / abs(elementary_charge_c)

    return {
        "initial_level": n_initial,
        "final_level": n_final,
        "process": process,
        "delta_energy_atom_j": delta_energy,
        "photon_energy_j": photon_energy,
        "photon_energy_ev": photon_energy_ev,
        "frequency_hz": frequency,
        "wavelength_m": wavelength,
        "wavelength_nm": wavelength * 1e9,
    }
