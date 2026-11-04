import pytest

from bohr_atom import PROTON_MASS_KG, BohrAtom


@pytest.fixture
def hydrogen():

    return BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG)


def test_emission(hydrogen):

    result = hydrogen.transition(3, 2)

    assert result["process"] == "emission"

    assert result["photon_energy_j"] > 0

    assert result["frequency_hz"] > 0

    assert result["wavelength_m"] > 0


def test_absorption(hydrogen):

    result = hydrogen.transition(2, 3)

    assert result["process"] == "absorption"


def test_energy_conservation(hydrogen):

    result = hydrogen.transition(3, 2)

    assert result["photon_energy_j"] == pytest.approx(
        abs(result["delta_energy_atom_j"])
    )


def test_photon_relations(hydrogen):

    result = hydrogen.transition(3, 2)

    h = hydrogen.planck_constant

    c = hydrogen.speed_of_light

    assert result["photon_energy_j"] == pytest.approx(h * result["frequency_hz"])

    assert result["wavelength_m"] == pytest.approx(c / result["frequency_hz"])
