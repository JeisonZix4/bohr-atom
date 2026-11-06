"""Pruebas de las visualizaciones 3D y de la cinemática orbital."""

import matplotlib

# El backend Agg permite validar figuras 3D sin abrir una ventana gráfica.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from bohr_atom import BohrAtom, PROTON_MASS_KG


def test_relative_orbital_speed_is_angular_speed_times_radius():
    """Verifica la relación cinemática v_rel = omega * r."""
    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hidrógeno")
    expected = atom.orbital_angular_frequency(2) * atom.radius(2, unit="m")
    assert atom.relative_orbital_speed(2) == pytest.approx(expected)


def test_static_3d_orbit_returns_3d_axes():
    """Comprueba que el método de BohrAtom produce ejes tridimensionales."""
    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hidrógeno")
    figure, axes = atom.plot_orbit_3d(n=2, inclination_deg=35.0)
    assert figure is axes.figure
    assert hasattr(axes, "get_zlim")
    assert axes.get_xlabel() == "x (pm)"
    plt.close(figure)


def test_static_3d_orbit_rejects_invalid_level():
    """Comprueba que el nivel cuántico cero se rechaza en el gráfico 3D."""
    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG)
    with pytest.raises(ValueError):
        atom.plot_orbit_3d(n=0)


def test_3d_animation_returns_func_animation():
    """Comprueba que la animación 3D devuelve un objeto FuncAnimation."""
    from matplotlib.animation import FuncAnimation

    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG)
    animation = atom.animate_orbit_3d(n=2, frames=12, interval=20)
    assert isinstance(animation, FuncAnimation)
    animation._init_draw()
    plt.close(animation._fig)


def test_3d_widget_viewer_requires_optional_dependencies_or_widget_backend():
    """Comprueba el control de dependencias del visor 3D de Jupyter."""
    from bohr_atom.interactive import interactive_orbit_3d_viewer

    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG)
    try:
        import ipywidgets  # noqa: F401
    except ImportError:
        with pytest.raises(ImportError):
            interactive_orbit_3d_viewer(atom, n_max=3)
        return

    with pytest.raises(RuntimeError, match="ipympl"):
        interactive_orbit_3d_viewer(atom, n_max=3)
