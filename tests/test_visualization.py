"""Pruebas básicas de las representaciones gráficas estáticas."""

import matplotlib

# El backend no interactivo permite ejecutar las pruebas en CI sin pantalla.
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from bohr_atom import BohrAtom, PROTON_MASS_KG


def test_energy_level_plot_returns_figure_and_axes():
    """Comprueba que el diagrama de niveles devuelve objetos Matplotlib."""
    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hidrógeno")
    figure, axes = atom.plot_energy_levels(n_max=4, transitions=[(3, 2)])
    assert figure is axes.figure
    assert axes.get_ylabel() == "Energía (eV)"
    plt.close(figure)


def test_orbit_plot_returns_equal_aspect_axes():
    """Comprueba que el gráfico orbital conserva la proporción geométrica."""
    atom = BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, name="Hidrógeno")
    figure, axes = atom.plot_orbits([1, 2, 3])
    assert figure is axes.figure
    assert axes.get_aspect() == 1.0
    plt.close(figure)
