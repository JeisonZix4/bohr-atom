"""Pruebas unitarias de los niveles energéticos del modelo de Bohr."""

import pytest

from bohr_atom import BohrAtom, PROTON_MASS_KG


@pytest.fixture
def hydrogen():
    """Construye una instancia de hidrógeno para las pruebas energéticas."""
    return BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hidrógeno")


def test_energy_is_negative(hydrogen):
    """Comprueba que los niveles ligados tienen energía negativa.

    Args:
        hydrogen: Fixture que proporciona una instancia de hidrógeno.
    """
    assert hydrogen.energy(1) < 0.0


def test_energy_scales_as_inverse_n_squared(hydrogen):
    """Verifica la dependencia analítica E_n proporcional a 1/n².

    Args:
        hydrogen: Fixture que proporciona una instancia de hidrógeno.
    """
    energy_1 = hydrogen.energy(1)
    assert hydrogen.energy(2) == pytest.approx(energy_1 / 4.0)
    assert hydrogen.energy(3) == pytest.approx(energy_1 / 9.0)


def test_energy_increases_toward_ionization_limit(hydrogen):
    """Comprueba que E_n aumenta y se acerca a cero al crecer n.

    Args:
        hydrogen: Fixture que proporciona una instancia de hidrógeno.
    """
    assert hydrogen.energy(2) > hydrogen.energy(1)
    assert hydrogen.energy(3) > hydrogen.energy(2)


def test_energy_unit_conversion(hydrogen):
    """Comprueba la conversión consistente entre julios y electronvoltios.

    Args:
        hydrogen: Fixture que proporciona una instancia de hidrógeno.
    """
    energy_j = hydrogen.energy(1, unit="J")
    energy_ev = hydrogen.energy(1, unit="eV")
    from bohr_atom.constants import ELEMENTARY_CHARGE_C

    assert energy_ev == pytest.approx(energy_j / ELEMENTARY_CHARGE_C)


def test_invalid_quantum_number_is_rejected(hydrogen):
    """Comprueba que n=0 no sea aceptado como número cuántico principal.

    Args:
        hydrogen: Fixture que proporciona una instancia de hidrógeno.
    """
    with pytest.raises(ValueError):
        hydrogen.energy(0)
