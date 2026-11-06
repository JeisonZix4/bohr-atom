"""Pruebas de rendimiento estructural de las animaciones orbitales."""

import matplotlib

# El backend Agg permite probar los artistas sin una ventana gráfica.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from bohr_atom import BohrAtom, PROTON_MASS_KG
from bohr_atom.interactive import animate_orbit, animate_orbit_3d


@pytest.fixture
def hydrogen():
    """Devuelve una instancia de hidrógeno para probar las animaciones."""
    return BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hidrógeno")


def test_2d_animation_uses_bounded_trail(hydrogen):
    """Comprueba que la estela 2D no crece indefinidamente."""
    animation = animate_orbit(
        hydrogen, n=2, frames=30, interval=20, trail_length=7
    )
    artists = animation._func(20)
    trail = artists[1]

    assert len(trail.get_xdata()) <= 7
    assert len(trail.get_ydata()) <= 7
    assert animation._interval == 20
    plt.close(animation._fig)


def test_3d_animation_uses_bounded_trail(hydrogen):
    """Comprueba que la estela 3D conserva un máximo de puntos fijo."""
    animation = animate_orbit_3d(
        hydrogen, n=2, frames=30, interval=20, trail_length=6
    )
    artists = animation._func(20)
    trail = artists[0]
    x_data, y_data, z_data = trail.get_data_3d()

    assert len(x_data) <= 6
    assert len(y_data) <= 6
    assert len(z_data) <= 6
    assert animation._interval == 20
    plt.close(animation._fig)


def test_animation_rejects_invalid_trail_length(hydrogen):
    """Comprueba que se rechazan longitudes de estela no positivas."""
    with pytest.raises(ValueError):
        animate_orbit(hydrogen, n=2, frames=20, trail_length=0)

    with pytest.raises(ValueError):
        animate_orbit_3d(hydrogen, n=2, frames=20, trail_length=0)
