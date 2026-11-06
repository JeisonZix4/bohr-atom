"""Pruebas de emisión, absorción y relaciones del fotón."""

import pytest

from bohr_atom import BohrAtom, PROTON_MASS_KG


@pytest.fixture
def hydrogen():
    """Construye una instancia de hidrógeno para probar transiciones."""
    return BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hidrógeno")


def test_downward_transition_is_emission(hydrogen):
    """Una transición desde n alto a n bajo debe producir emisión."""
    result = hydrogen.transition(3, 2)
    assert result["process"] == "emission"
    assert result["delta_energy_atom_j"] < 0.0
    assert result["photon_energy_j"] > 0.0


def test_upward_transition_is_absorption(hydrogen):
    """Una transición desde n bajo a n alto debe requerir absorción."""
    result = hydrogen.transition(2, 3)
    assert result["process"] == "absorption"
    assert result["delta_energy_atom_j"] > 0.0
    assert result["photon_energy_j"] > 0.0


def test_photon_energy_matches_absolute_atomic_energy_change(hydrogen):
    """Comprueba que E_fotón=|E_final-E_inicial|."""
    result = hydrogen.transition(4, 2)
    assert result["photon_energy_j"] == pytest.approx(
        abs(result["delta_energy_atom_j"])
    )


def test_photon_energy_frequency_and_wavelength_are_consistent(hydrogen):
    """Verifica E=hν y λ=c/ν para una transición permitida."""
    result = hydrogen.transition(3, 2)
    assert result["photon_energy_j"] == pytest.approx(
        hydrogen.planck_constant * result["frequency_hz"]
    )
    assert result["wavelength_m"] == pytest.approx(
        hydrogen.speed_of_light / result["frequency_hz"]
    )


def test_same_initial_and_final_level_is_rejected(hydrogen):
    """Una transición entre el mismo nivel no debe aceptarse."""
    with pytest.raises(ValueError):
        hydrogen.transition(2, 2)
