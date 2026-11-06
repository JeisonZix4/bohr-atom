import pytest

from bohr_atom import BohrAtom, PROTON_MASS_KG


@pytest.fixture
def hydrogen():
    return BohrAtom(
        Z=1,
        nucleus_mass_kg=PROTON_MASS_KG,
        name="Hidrógeno",
    )


def test_orbital_angular_frequency_is_positive(hydrogen):
    assert hydrogen.orbital_angular_frequency(1) > 0


def test_orbital_angular_frequency_scales_as_inverse_n_cubed(hydrogen):
    omega_1 = hydrogen.orbital_angular_frequency(1)
    omega_2 = hydrogen.orbital_angular_frequency(2)
    omega_3 = hydrogen.orbital_angular_frequency(3)

    assert omega_2 == pytest.approx(omega_1 / 8)
    assert omega_3 == pytest.approx(omega_1 / 27)


def test_orbital_period_is_positive(hydrogen):
    assert hydrogen.orbital_period(1) > 0


def test_orbital_period_scales_as_n_cubed(hydrogen):
    period_1 = hydrogen.orbital_period(1)
    period_2 = hydrogen.orbital_period(2)

    assert period_2 == pytest.approx(8 * period_1)


def test_orbital_period_and_angular_frequency_are_reciprocal(hydrogen):
    omega = hydrogen.orbital_angular_frequency(2)
    period = hydrogen.orbital_period(2)

    import math

    assert period == pytest.approx(2 * math.pi / omega)


def test_invalid_quantum_number_for_orbital_frequency(hydrogen):
    with pytest.raises(ValueError):
        hydrogen.orbital_angular_frequency(0)
