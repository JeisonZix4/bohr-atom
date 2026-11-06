"""Pruebas de inicialización y validación de la clase BohrAtom."""

import pytest

from bohr_atom import BohrAtom, PROTON_MASS_KG


def test_atom_initialization():
    """Comprueba que se almacenen los parámetros del sistema."""
    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hidrógeno")
    assert atom.Z == 1
    assert atom.name == "Hidrógeno"
    assert atom.nuclear_charge_c > 0.0
    assert atom.electron_charge_c < 0.0
    assert atom.reduced_mass_kg > 0.0


def test_energy_levels_returns_expected_fields():
    """Comprueba la estructura de los datos devueltos para varios niveles."""
    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG)
    levels = atom.energy_levels(n_max=3)
    assert len(levels) == 3
    assert set(levels[0]) == {"n", "energy", "energy_unit", "radius_pm"}


def test_invalid_atomic_number_is_rejected():
    """El número atómico debe ser un entero positivo."""
    with pytest.raises(ValueError):
        BohrAtom(Z=0, nucleus_mass_kg=PROTON_MASS_KG)


def test_invalid_nuclear_mass_is_rejected():
    """La masa nuclear debe ser finita y estrictamente positiva."""
    with pytest.raises(ValueError):
        BohrAtom(Z=1, nucleus_mass_kg=-1.0)


def test_empty_atom_name_is_rejected():
    """La etiqueta descriptiva no puede ser una cadena vacía."""
    with pytest.raises(ValueError):
        BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="  ")
