"""Pruebas unitarias de radios y cinemática orbital."""

import pytest

from bohr_atom import BohrAtom, PROTON_MASS_KG


@pytest.fixture
def hydrogen():
    """Construye una instancia de hidrógeno para las pruebas orbitales."""
    return BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hidrógeno")


def test_radius_scales_as_n_squared(hydrogen):
    """Verifica que el radio de Bohr crece proporcionalmente a n²."""
    radius_1 = hydrogen.radius(1)
    assert hydrogen.radius(2) == pytest.approx(4.0 * radius_1)
    assert hydrogen.radius(3) == pytest.approx(9.0 * radius_1)


def test_radius_is_positive(hydrogen):
    """Comprueba que una órbita permitida tiene radio positivo."""
    assert hydrogen.radius(1) > 0.0


def test_radius_unit_conversion(hydrogen):
    """Comprueba que el mismo radio se obtiene en m y pm."""
    radius_m = hydrogen.radius(1, unit="m")
    radius_pm = hydrogen.radius(1, unit="pm")
    assert radius_pm == pytest.approx(radius_m * 1e12)


def test_angular_frequency_scales_as_inverse_n_cubed(hydrogen):
    """Verifica la dependencia omega_n proporcional a 1/n³."""
    omega_1 = hydrogen.orbital_angular_frequency(1)
    assert hydrogen.orbital_angular_frequency(2) == pytest.approx(omega_1 / 8.0)
    assert hydrogen.orbital_angular_frequency(3) == pytest.approx(omega_1 / 27.0)


def test_period_and_angular_frequency_are_consistent(hydrogen):
    """Comprueba que el período orbital cumple T=2π/omega."""
    import math

    omega = hydrogen.orbital_angular_frequency(2)
    period = hydrogen.orbital_period(2)
    assert period == pytest.approx(2.0 * math.pi / omega)


def test_invalid_level_for_orbital_dynamics_is_rejected(hydrogen):
    """Comprueba que el nivel n=0 también se rechaza en la cinemática."""
    with pytest.raises(ValueError):
        hydrogen.orbital_period(0)
