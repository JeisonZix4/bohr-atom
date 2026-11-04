import pytest

from bohr_atom import PROTON_MASS_KG, BohrAtom


@pytest.fixture
def hydrogen():

    return BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hydrogen")


def test_energy_is_negative(hydrogen):

    assert hydrogen.energy(1) < 0


def test_energy_scaling(hydrogen):

    E1 = hydrogen.energy(1)

    E2 = hydrogen.energy(2)

    E3 = hydrogen.energy(3)

    assert E2 == pytest.approx(E1 / 4)

    assert E3 == pytest.approx(E1 / 9)


def test_energy_increases_with_n(hydrogen):

    assert hydrogen.energy(2) > hydrogen.energy(1)


def test_invalid_quantum_number(hydrogen):

    with pytest.raises(ValueError):
        hydrogen.energy(0)
