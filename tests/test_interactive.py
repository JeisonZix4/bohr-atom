"""Pruebas de las funciones de animación e interacción del modelo de Bohr."""

import math

import matplotlib

# Se selecciona un backend sin interfaz gráfica para ejecutar pruebas en CI.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from bohr_atom import BohrAtom, PROTON_MASS_KG
from bohr_atom.interactive import _phase_coordinates


def test_animate_orbit_returns_matplotlib_animation():
    """Verifica que animate_orbit construye un objeto FuncAnimation."""
    animation_module = pytest.importorskip("matplotlib.animation")
    from bohr_atom.interactive import animate_orbit

    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hidrógeno")
    animation = animate_orbit(atom, n=2, frames=12, interval=20)
    assert isinstance(animation, animation_module.FuncAnimation)
    # Ejecuta el dibujo inicial y evita una advertencia de animación sin renderizar.
    animation._init_draw()
    plt.close(animation._fig)


def test_phase_coordinates_at_quarter_turn():
    """Comprueba que la fase π/2 sitúa el electrón sobre el eje y positivo."""
    x_position, y_position = _phase_coordinates(radius=4.0, phase=math.pi / 2.0)
    assert x_position == pytest.approx(0.0, abs=1e-9)
    assert y_position == pytest.approx(4.0)


def test_widget_viewer_requires_interactive_backend():
    """Comprueba que el visor avisa si Matplotlib usa un backend estático."""
    from bohr_atom.interactive import interactive_orbit_viewer

    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG)
    pytest.importorskip("ipywidgets")
    with pytest.raises(RuntimeError, match="ipympl"):
        interactive_orbit_viewer(atom, n_max=3)
