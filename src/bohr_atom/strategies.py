"""Estrategias de cálculo para el modelo de Bohr.

Este módulo implementa el patrón de diseño Strategy en el núcleo del paquete.
Cada estrategia define cómo se obtiene la masa efectiva y delega en las
funciones físicas compartidas el cálculo de energía, radio y velocidad angular.
La clase :class:`BohrAtom` utiliza estas operaciones en sus métodos públicos.
"""

from typing import Protocol, runtime_checkable

from .energy import energy_level_joule, reduced_mass
from .orbit import orbital_angular_frequency_rad_s, orbital_radius_m
from .validation import validate_positive_real


@runtime_checkable
class MassStrategy(Protocol):
    """Interfaz compatible con estrategias de masa de versiones anteriores."""

    def calculate(self, electron_mass_kg: float, nucleus_mass_kg: float) -> float:
        """Calcula la masa efectiva en kilogramos.

        Args:
            electron_mass_kg: Masa del electrón en kilogramos.
            nucleus_mass_kg: Masa del núcleo en kilogramos.

        Returns:
            float: Masa efectiva en kilogramos.
        """
        ...


@runtime_checkable
class BohrCalculationStrategy(Protocol):
    """Interfaz de cálculo que utiliza directamente la clase ``BohrAtom``.

    La estrategia define las operaciones que producen energía, radio y
    velocidad angular. Así, el patrón Strategy participa en el flujo real de
    cálculo de la biblioteca, en lugar de limitarse a una demostración aislada
    de cómo seleccionar la masa efectiva.
    """

    def effective_mass(self, electron_mass_kg: float, nucleus_mass_kg: float) -> float:
        """Devuelve la masa efectiva en kilogramos."""
        ...

    def calculate_energy(self, *, n: int, Z: int, electron_mass_kg: float,
                         nucleus_mass_kg: float, elementary_charge_c: float,
                         epsilon_0: float, hbar: float) -> float:
        """Calcula la energía del nivel ``n`` en julios."""
        ...

    def calculate_radius(self, *, n: int, Z: int, electron_mass_kg: float,
                         nucleus_mass_kg: float, elementary_charge_c: float,
                         epsilon_0: float, hbar: float) -> float:
        """Calcula la separación relativa electrón-núcleo en metros."""
        ...

    def calculate_angular_frequency(self, *, n: int, Z: int,
                                    electron_mass_kg: float,
                                    nucleus_mass_kg: float,
                                    elementary_charge_c: float,
                                    epsilon_0: float, hbar: float) -> float:
        """Calcula la velocidad angular relativa en rad/s."""
        ...


class _BaseBohrStrategy:
    """Implementa las operaciones comunes de las estrategias concretas.

    Las subclases únicamente definen la masa efectiva. Los tres cálculos
    principales se ejecutan mediante las funciones matemáticas compartidas,
    garantizando que las ecuaciones no se dupliquen entre estrategias.
    """

    def effective_mass(self, electron_mass_kg: float, nucleus_mass_kg: float) -> float:
        """Obtiene la masa efectiva; las subclases deben implementar este método."""
        raise NotImplementedError

    def calculate(self, electron_mass_kg: float, nucleus_mass_kg: float) -> float:
        """Mantiene la interfaz de masa utilizada en versiones anteriores.

        Args:
            electron_mass_kg: Masa del electrón en kilogramos.
            nucleus_mass_kg: Masa del núcleo en kilogramos.

        Returns:
            float: Masa efectiva en kilogramos.
        """
        return self.effective_mass(electron_mass_kg, nucleus_mass_kg)

    def calculate_energy(self, *, n: int, Z: int, electron_mass_kg: float,
                         nucleus_mass_kg: float, elementary_charge_c: float,
                         epsilon_0: float, hbar: float) -> float:
        """Calcula el nivel energético usando la aproximación seleccionada.

        Args:
            n: Número cuántico principal positivo.
            Z: Número atómico positivo.
            electron_mass_kg: Masa del electrón en kilogramos.
            nucleus_mass_kg: Masa del núcleo en kilogramos.
            elementary_charge_c: Carga elemental en culombios.
            epsilon_0: Permitividad del vacío en F/m.
            hbar: Constante de Planck reducida en J s.

        Returns:
            float: Energía del estado ligado en julios.
        """
        mu = self.effective_mass(electron_mass_kg, nucleus_mass_kg)
        return energy_level_joule(n, Z, mu, elementary_charge_c, epsilon_0, hbar)

    def calculate_radius(self, *, n: int, Z: int, electron_mass_kg: float,
                         nucleus_mass_kg: float, elementary_charge_c: float,
                         epsilon_0: float, hbar: float) -> float:
        """Calcula el radio orbital usando la aproximación seleccionada.

        Args:
            n: Número cuántico principal positivo.
            Z: Número atómico positivo.
            electron_mass_kg: Masa del electrón en kilogramos.
            nucleus_mass_kg: Masa del núcleo en kilogramos.
            elementary_charge_c: Carga elemental en culombios.
            epsilon_0: Permitividad del vacío en F/m.
            hbar: Constante de Planck reducida en J s.

        Returns:
            float: Separación relativa electrón-núcleo en metros.
        """
        mu = self.effective_mass(electron_mass_kg, nucleus_mass_kg)
        return orbital_radius_m(n, Z, mu, elementary_charge_c, epsilon_0, hbar)

    def calculate_angular_frequency(self, *, n: int, Z: int,
                                    electron_mass_kg: float,
                                    nucleus_mass_kg: float,
                                    elementary_charge_c: float,
                                    epsilon_0: float, hbar: float) -> float:
        """Calcula la velocidad angular usando la aproximación seleccionada.

        Args:
            n: Número cuántico principal positivo.
            Z: Número atómico positivo.
            electron_mass_kg: Masa del electrón en kilogramos.
            nucleus_mass_kg: Masa del núcleo en kilogramos.
            elementary_charge_c: Carga elemental en culombios.
            epsilon_0: Permitividad del vacío en F/m.
            hbar: Constante de Planck reducida en J s.

        Returns:
            float: Velocidad angular orbital en rad/s.
        """
        mu = self.effective_mass(electron_mass_kg, nucleus_mass_kg)
        return orbital_angular_frequency_rad_s(
            n, Z, mu, elementary_charge_c, epsilon_0, hbar
        )


class ReducedMassStrategy(_BaseBohrStrategy):
    """Calcula energía, radio y dinámica con la masa reducida.

    Esta es la estrategia predeterminada. Considera el movimiento de ambos
    cuerpos alrededor del centro de masa mediante la coordenada relativa.
    """

    def effective_mass(self, electron_mass_kg: float, nucleus_mass_kg: float) -> float:
        """Calcula la masa reducida ``m_e M / (m_e + M)``.

        Args:
            electron_mass_kg: Masa del electrón en kilogramos.
            nucleus_mass_kg: Masa del núcleo en kilogramos.

        Returns:
            float: Masa reducida en kilogramos.
        """
        return reduced_mass(electron_mass_kg, nucleus_mass_kg)


class InfiniteNucleusMassStrategy(_BaseBohrStrategy):
    """Aplica la aproximación de núcleo inmóvil o masa nuclear infinita.

    En esta aproximación, energía, radio y velocidad angular se calculan con
    la masa del electrón, sin corrección por retroceso del núcleo.
    """

    def effective_mass(self, electron_mass_kg: float, nucleus_mass_kg: float) -> float:
        """Devuelve la masa electrónica después de validar ambas masas.

        Args:
            electron_mass_kg: Masa del electrón en kilogramos.
            nucleus_mass_kg: Masa del núcleo en kilogramos; se valida aunque
                no intervenga en el resultado de esta aproximación.

        Returns:
            float: Masa del electrón en kilogramos.
        """
        electron_mass = validate_positive_real(electron_mass_kg, "electron_mass_kg")
        validate_positive_real(nucleus_mass_kg, "nucleus_mass_kg")
        return electron_mass


class _LegacyMassStrategyAdapter(_BaseBohrStrategy):
    """Adapta estrategias antiguas que únicamente implementaban ``calculate``."""

    def __init__(self, legacy_strategy: MassStrategy) -> None:
        """Almacena la estrategia anterior que se desea adaptar.

        Args:
            legacy_strategy: Objeto con un método ``calculate`` compatible.

        Raises:
            TypeError: Si el objeto no implementa el método ``calculate``.
        """
        if not callable(getattr(legacy_strategy, "calculate", None)):
            raise TypeError("La estrategia antigua debe implementar calculate().")
        self._legacy_strategy = legacy_strategy

    def effective_mass(self, electron_mass_kg: float, nucleus_mass_kg: float) -> float:
        """Obtiene la masa efectiva mediante la interfaz anterior.

        Args:
            electron_mass_kg: Masa del electrón en kilogramos.
            nucleus_mass_kg: Masa del núcleo en kilogramos.

        Returns:
            float: Masa efectiva en kilogramos.
        """
        return self._legacy_strategy.calculate(electron_mass_kg, nucleus_mass_kg)
