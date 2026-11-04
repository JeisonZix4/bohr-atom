import pytest

from bohr_atom import PROTON_MASS_KG, BohrAtom


def test_radius_scaling():

    hydrogen = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG)

    r1 = hydrogen.radius(1)

    r2 = hydrogen.radius(2)

    r3 = hydrogen.radius(3)

    assert r2 == pytest.approx(4 * r1)

    assert r3 == pytest.approx(9 * r1)


def test_radius_is_positive():

    hydrogen = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG)

    assert hydrogen.radius(1) > 0
