"""Pruebas de integración del patrón Strategy en la clase BohrAtom."""

import pytest

from bohr_atom import (
    BohrAtom,
    BohrCalculationStrategy,
    InfiniteNucleusMassStrategy,
    PROTON_MASS_KG,
    ReducedMassStrategy,
)
from bohr_atom.constants import ELECTRON_MASS_KG


def make_hydrogen(**kwargs):
    """Construye hidrógeno con parámetros comunes para las pruebas.

    Args:
        **kwargs: Argumentos adicionales que se transfieren a ``BohrAtom``.

    Returns:
        BohrAtom: Instancia de hidrógeno.
    """
    return BohrAtom(Z=1, nucleus_mass_kg=PROTON_MASS_KG, **kwargs)


def test_reduced_mass_strategy_is_the_default():
    """Comprueba que la estrategia predeterminada usa masa reducida."""
    atom = make_hydrogen()
    expected = (
        ELECTRON_MASS_KG * PROTON_MASS_KG
        / (ELECTRON_MASS_KG + PROTON_MASS_KG)
    )

    assert isinstance(atom.calculation_strategy, ReducedMassStrategy)
    assert atom.calculation_strategy_name == "ReducedMassStrategy"
    assert atom.effective_mass_kg == pytest.approx(expected)


def test_strategy_is_used_by_energy_radius_and_orbital_dynamics():
    """Comprueba que una estrategia cambia todos los cálculos del átomo.

    La aproximación de núcleo inmóvil debe producir niveles más profundos,
    radios menores y velocidades angulares mayores que la masa reducida.
    """
    finite_nucleus = make_hydrogen(
        calculation_strategy=ReducedMassStrategy()
    )
    fixed_nucleus = make_hydrogen(
        calculation_strategy=InfiniteNucleusMassStrategy()
    )

    assert fixed_nucleus.energy(1) < finite_nucleus.energy(1)
    assert fixed_nucleus.radius(1) < finite_nucleus.radius(1)
    assert (
        fixed_nucleus.orbital_angular_frequency(1)
        > finite_nucleus.orbital_angular_frequency(1)
    )


def test_transition_uses_the_selected_calculation_strategy():
    """Comprueba que la estrategia también afecta el fotón de una transición."""
    finite_nucleus = make_hydrogen(
        calculation_strategy=ReducedMassStrategy()
    )
    fixed_nucleus = make_hydrogen(
        calculation_strategy=InfiniteNucleusMassStrategy()
    )

    transition_finite = finite_nucleus.transition(3, 2)
    transition_fixed = fixed_nucleus.transition(3, 2)

    assert transition_fixed["photon_energy_ev"] > transition_finite["photon_energy_ev"]
    assert transition_fixed["wavelength_m"] < transition_finite["wavelength_m"]


def test_energy_levels_and_visualization_use_the_context_strategy():
    """Comprueba que las operaciones agregadas usan la estrategia del átomo."""
    atom = make_hydrogen(
        calculation_strategy=InfiniteNucleusMassStrategy()
    )

    levels = atom.energy_levels(n_max=3)
    assert levels[0]["energy"] == pytest.approx(atom.energy(1))
    assert levels[0]["radius_pm"] == pytest.approx(atom.radius(1, "pm"))

    figure, axes = atom.plot_energy_levels(n_max=3, transitions=[(3, 2)])
    assert figure is axes.figure
    figure.clear()


def test_legacy_mass_strategy_argument_remains_compatible():
    """Mantiene compatibilidad con el argumento mass_strategy anterior."""
    atom = make_hydrogen(mass_strategy=InfiniteNucleusMassStrategy())
    assert atom.calculation_strategy_name == "InfiniteNucleusMassStrategy"
    assert atom.effective_mass_kg == pytest.approx(ELECTRON_MASS_KG)


def test_legacy_custom_calculate_strategy_is_adapted():
    """Adapta una estrategia externa que solo implementaba calculate()."""

    class LegacyElectronMassStrategy:
        """Estrategia antigua mínima para comprobar compatibilidad."""

        def calculate(self, electron_mass_kg, nucleus_mass_kg):
            """Devuelve la masa electrónica e ignora la masa nuclear."""
            del nucleus_mass_kg
            return electron_mass_kg

    atom = make_hydrogen(mass_strategy=LegacyElectronMassStrategy())
    assert atom.effective_mass_kg == pytest.approx(ELECTRON_MASS_KG)
    assert atom.energy(1) == pytest.approx(-13.605693, rel=2e-5)


def test_invalid_strategy_is_rejected():
    """Rechaza objetos que no satisfacen ninguna interfaz de estrategia."""
    with pytest.raises(TypeError, match="calculate"):
        make_hydrogen(mass_strategy=object())


def test_both_strategy_arguments_cannot_be_combined():
    """Evita ambigüedad si se suministran los dos argumentos."""
    with pytest.raises(ValueError, match="no ambos"):
        make_hydrogen(
            calculation_strategy=ReducedMassStrategy(),
            mass_strategy=InfiniteNucleusMassStrategy(),
        )


def test_strategy_protocol_is_public():
    """Comprueba que las estrategias concretas implementan el protocolo público."""
    strategy = ReducedMassStrategy()
    assert isinstance(strategy, BohrCalculationStrategy)
