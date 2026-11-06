"""Pruebas mínimas de la generación de animaciones orbitales."""

import matplotlib

# Se selecciona un backend sin interfaz gráfica para entornos automatizados.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from bohr_atom import BohrAtom, PROTON_MASS_KG


def test_animate_orbit_returns_matplotlib_animation():
    """Verifica que animate_orbit construye un objeto FuncAnimation."""
    animation_module = pytest.importorskip("matplotlib.animation")
    from bohr_atom.interactive import animate_orbit

    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hidrógeno")
    animation = animate_orbit(atom, n=2, frames=12, interval=20)
    assert isinstance(animation, animation_module.FuncAnimation)
    # Ejecuta el dibujo inicial para verificar la inicialización del objeto
    # y evitar que Matplotlib advierta que la animación se descartó sin render.
    animation._init_draw()
    plt.close(animation._fig)
