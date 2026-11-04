import pytest

from bohr_atom import PROTON_MASS_KG, BohrAtom


def test_atom_initialization():

    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hydrogen")

    assert atom.Z == 1

    assert atom.name == "Hydrogen"

    assert atom.nuclear_charge_c > 0

    assert atom.electron_charge_c < 0


def test_reduced_mass_is_positive():

    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG)

    assert atom.reduced_mass_kg > 0


def test_invalid_atomic_number():

    with pytest.raises(ValueError):
        BohrAtom(Z=0, nucleus_mass_kg=PROTON_MASS_KG)


def test_invalid_nuclear_mass():

    with pytest.raises(ValueError):
        BohrAtom(Z=1, nucleus_mass_kg=-1)
