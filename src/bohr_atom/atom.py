"""Clase de alto nivel para representar átomos e iones hidrogenoides.

La clase reúne parámetros del sistema y ofrece una interfaz coherente para
calcular energías, radios, transiciones y gráficos sin duplicar ecuaciones.
"""

from .constants import (
    ELECTRON_MASS_KG,
    ELEMENTARY_CHARGE_C,
    PLANCK_CONSTANT_J_S,
    REDUCED_PLANCK_CONSTANT_J_S,
    SPEED_OF_LIGHT_M_S,
    VACUUM_PERMITTIVITY_F_M,
)
from .orbit import convert_radius, orbital_period_s
from .strategies import (
    BohrCalculationStrategy,
    MassStrategy,
    ReducedMassStrategy,
    _LegacyMassStrategyAdapter,
)
from .transitions import transition_properties
from .validation import validate_positive_integer, validate_positive_real


class BohrAtom:
    """Representa un sistema de un electrón mediante el modelo de Bohr.

    Args:
        Z: Número atómico del núcleo. El sistema contiene un único electrón;
            la carga nuclear es ``+Z e``.
        nucleus_mass_kg: Masa del núcleo en kilogramos.
        name: Etiqueta descriptiva utilizada en las representaciones gráficas.
        electron_mass_kg: Masa del electrón en kilogramos. Por defecto usa
            el valor recomendado por CODATA.
        calculation_strategy: Estrategia que realiza los cálculos de energía,
            radio y velocidad angular. Por defecto utiliza masa reducida.
        mass_strategy: Alias de compatibilidad con versiones anteriores; se
            recomienda utilizar ``calculation_strategy`` en código nuevo.

    Note:
        Las fórmulas utilizan la masa efectiva seleccionada y describen la
        coordenada relativa electrón-núcleo. Por defecto la estrategia calcula
        la masa reducida; la estrategia de núcleo inmóvil utiliza la masa del
        electrón. La estrategia seleccionada interviene directamente en energía,
        radio y velocidad angular. El modelo es no relativista y no incluye
        estructura fina, hiperfina ni efectos de tamaño nuclear.
    """

    def __init__(
        self,
        Z: int,
        nucleus_mass_kg: float,
        name: str = "Sistema hidrogenoide",
        electron_mass_kg: float = ELECTRON_MASS_KG,
        calculation_strategy: BohrCalculationStrategy | None = None,
        mass_strategy: MassStrategy | None = None,
    ) -> None:
        """Inicializa el sistema hidrogenoide y configura su estrategia de cálculo.

        Args:
            Z: Número atómico del núcleo. Debe ser un entero positivo.
            nucleus_mass_kg: Masa del núcleo en kilogramos.
            name: Nombre descriptivo utilizado en las salidas y los gráficos.
            electron_mass_kg: Masa del electrón en kilogramos. Por defecto usa
                el valor recomendado por CODATA.
            calculation_strategy: Estrategia completa para los cálculos físicos.
                Por defecto se utiliza ``ReducedMassStrategy``.
            mass_strategy: Nombre anterior del argumento, conservado para
                compatibilidad. No debe combinarse con calculation_strategy.

        Raises:
            TypeError: Si Z o las masas tienen tipos inválidos, o si la estrategia
                no implementa los métodos de cálculo requeridos.
            ValueError: Si Z o alguna masa no es positiva, si name está vacío,
                o si se proporcionan ambos argumentos de estrategia.
        """
        self.Z = validate_positive_integer(Z, "Z")
        self.nucleus_mass_kg = validate_positive_real(
            nucleus_mass_kg, "nucleus_mass_kg"
        )
        self.electron_mass_kg = validate_positive_real(
            electron_mass_kg, "electron_mass_kg"
        )
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name debe ser una cadena no vacía.")
        self.name = name.strip()

        # Las cargas conservan sus signos: el núcleo es positivo y el electrón negativo.
        self.electron_charge_c = -ELEMENTARY_CHARGE_C
        self.nuclear_charge_c = self.Z * ELEMENTARY_CHARGE_C

        # Se conservan las constantes en la instancia para hacer explícito
        # qué parámetros físicos utiliza cada objeto.
        self.epsilon_0 = VACUUM_PERMITTIVITY_F_M
        self.planck_constant = PLANCK_CONSTANT_J_S
        self.hbar = REDUCED_PLANCK_CONSTANT_J_S
        self.speed_of_light = SPEED_OF_LIGHT_M_S

        # Strategy forma parte del flujo normal de cálculo de BohrAtom.
        # La misma estrategia se utiliza para energía, radio y velocidad angular.
        if calculation_strategy is not None and mass_strategy is not None:
            raise ValueError(
                "Utiliza calculation_strategy o mass_strategy, pero no ambos."
            )

        selected_strategy = calculation_strategy
        if selected_strategy is None and mass_strategy is not None:
            required_methods = (
                "effective_mass",
                "calculate_energy",
                "calculate_radius",
                "calculate_angular_frequency",
            )
            if all(
                callable(getattr(mass_strategy, method, None))
                for method in required_methods
            ):
                selected_strategy = mass_strategy
            else:
                # Adapta estrategias anteriores que solo definían calculate().
                selected_strategy = _LegacyMassStrategyAdapter(mass_strategy)

        if selected_strategy is None:
            selected_strategy = ReducedMassStrategy()

        required_methods = (
            "effective_mass",
            "calculate_energy",
            "calculate_radius",
            "calculate_angular_frequency",
        )
        missing_methods = [
            method
            for method in required_methods
            if not callable(getattr(selected_strategy, method, None))
        ]
        if missing_methods:
            raise TypeError(
                "calculation_strategy no implementa la interfaz requerida. "
                f"Faltan los métodos: {', '.join(missing_methods)}."
            )

        self.calculation_strategy = selected_strategy
        # Alias del nombre anterior para conservar compatibilidad de acceso.
        self.mass_strategy = selected_strategy

        self.effective_mass_kg = validate_positive_real(
            self.calculation_strategy.effective_mass(
                self.electron_mass_kg,
                self.nucleus_mass_kg,
            ),
            "masa efectiva calculada por calculation_strategy",
        )
        # Alias histórico: con la estrategia de núcleo inmóvil representa m_e.
        self.reduced_mass_kg = self.effective_mass_kg

    @property
    def calculation_strategy_name(self) -> str:
        """Devuelve el nombre de la estrategia usada por el objeto.

        Returns:
            str: Nombre de la clase de estrategia seleccionada.
        """
        return type(self.calculation_strategy).__name__

    def __repr__(self) -> str:
        """Devuelve una representación breve y útil para depuración."""
        return (
            f"BohrAtom(name={self.name!r}, Z={self.Z}, "
            f"effective_mass={self.effective_mass_kg:.6e} kg, "
            f"strategy={type(self.calculation_strategy).__name__})"
        )

    def energy(self, n: int, unit: str = "eV") -> float:
        """Calcula la energía del nivel principal ``n``.

        Args:
            n: Número cuántico principal positivo.
            unit: Unidad de salida: ``'J'`` para julios o ``'eV'`` para electronvoltios.

        Returns:
            float: Energía del estado ligado en la unidad solicitada.
        """
        energy_joule = self.calculation_strategy.calculate_energy(
            n=n,
            Z=self.Z,
            electron_mass_kg=self.electron_mass_kg,
            nucleus_mass_kg=self.nucleus_mass_kg,
            elementary_charge_c=self.electron_charge_c,
            epsilon_0=self.epsilon_0,
            hbar=self.hbar,
        )
        if not isinstance(unit, str):
            raise TypeError("unit debe ser una cadena: 'J' o 'eV'.")
        normalized_unit = unit.lower()
        if normalized_unit == "j":
            return energy_joule
        if normalized_unit == "ev":
            return energy_joule / ELEMENTARY_CHARGE_C
        raise ValueError("La unidad de energía debe ser 'J' o 'eV'.")

    def radius(self, n: int, unit: str = "m") -> float:
        """Calcula la distancia relativa electrón-núcleo del nivel ``n``.

        Args:
            n: Número cuántico principal positivo.
            unit: Unidad de salida: ``m``, ``nm``, ``pm`` o ``angstrom``.

        Returns:
            float: Radio o separación relativa en la unidad solicitada.
        """
        radius_m = self.calculation_strategy.calculate_radius(
            n=n,
            Z=self.Z,
            electron_mass_kg=self.electron_mass_kg,
            nucleus_mass_kg=self.nucleus_mass_kg,
            elementary_charge_c=self.electron_charge_c,
            epsilon_0=self.epsilon_0,
            hbar=self.hbar,
        )
        return convert_radius(radius_m, unit)

    def orbital_angular_frequency(self, n: int) -> float:
        """Calcula la velocidad angular relativa de la órbita, en radianes por segundo.

        No debe confundirse con la frecuencia del fotón emitido o absorbido durante
        una transición entre niveles.

        Args:
            n: Número cuántico principal positivo.

        Returns:
            float: Velocidad angular orbital relativa en rad/s.

        Raises:
            TypeError: Si n no es un entero.
            ValueError: Si n no es positivo.
        """
        return self.calculation_strategy.calculate_angular_frequency(
            n=n,
            Z=self.Z,
            electron_mass_kg=self.electron_mass_kg,
            nucleus_mass_kg=self.nucleus_mass_kg,
            elementary_charge_c=self.electron_charge_c,
            epsilon_0=self.epsilon_0,
            hbar=self.hbar,
        )

    def relative_orbital_speed(self, n: int) -> float:
        """Calcula la rapidez tangencial de la coordenada relativa.

        Args:
            n: Número cuántico principal positivo.

        Returns:
            float: Rapidez relativa electrón-núcleo en metros por segundo.

        Note:
            Se calcula como ``v_rel = omega * r``. No debe confundirse con
            la velocidad visual de la animación ni con la rapidez del fotón.
        """
        radius_m = self.radius(n, unit="m")
        return self.orbital_angular_frequency(n) * radius_m

    def orbital_period(self, n: int) -> float:
        """Calcula el período de revolución relativo para el nivel n.

        Args:
            n: Número cuántico principal positivo.

        Returns:
            float: Período orbital en segundos.

        Raises:
            TypeError: Si n no es un entero.
            ValueError: Si n no es positivo.
        """
        return orbital_period_s(self.orbital_angular_frequency(n))

    def energy_levels(self, n_max: int = 5, energy_unit: str = "eV") -> list[dict]:
        """Genera una lista con energías y radios para los niveles 1 a ``n_max``.

        Args:
            n_max: Último número cuántico principal que se incluirá.
            energy_unit: Unidad de las energías: ``'J'`` o ``'eV'``.

        Returns:
            list[dict]: Cada diccionario contiene ``n``, ``energy``, ``energy_unit``
                y ``radius_pm``. Se devuelve una lista para evitar que Pandas
                sea una dependencia de la biblioteca principal.
        """
        n_max = validate_positive_integer(n_max, "n_max")
        if not isinstance(energy_unit, str):
            raise TypeError("energy_unit debe ser una cadena.")
        normalized_unit = energy_unit.lower()
        if normalized_unit not in {"j", "ev"}:
            raise ValueError("energy_unit debe ser 'J' o 'eV'.")

        return [
            {
                "n": n,
                "energy": self.energy(n, unit=normalized_unit),
                "energy_unit": normalized_unit,
                "radius_pm": self.radius(n, unit="pm"),
            }
            for n in range(1, n_max + 1)
        ]

    def transition(self, n_initial: int, n_final: int) -> dict:
        """Calcula las propiedades del fotón asociado a una transición entre niveles.

        La variación de energía del átomo se define como E_final - E_inicial.
        Una transición descendente produce emisión; una ascendente requiere
        absorción.

        Args:
            n_initial: Número cuántico principal del estado inicial.
            n_final: Número cuántico principal del estado final.

        Returns:
            dict: Propiedades de la transición: proceso, variación energética del
                átomo, energía del fotón, frecuencia y longitud de onda.

        Raises:
            TypeError: Si alguno de los números cuánticos no es entero.
            ValueError: Si los niveles no son positivos o son iguales.
        """
        energy_initial = self.energy(n_initial, unit="J")
        energy_final = self.energy(n_final, unit="J")
        return transition_properties(
            n_initial=n_initial,
            n_final=n_final,
            energy_initial_j=energy_initial,
            energy_final_j=energy_final,
            h=self.planck_constant,
            c=self.speed_of_light,
            elementary_charge_c=ELEMENTARY_CHARGE_C,
        )

    def plot_energy_levels(self, n_max: int = 5, transitions=None, ax=None):
        """Representa los niveles energéticos y las transiciones con Matplotlib.

        Args:
            n_max: Último número cuántico principal que se dibujará.
            transitions: Pares opcionales (n_inicial, n_final). Si es None, se
                muestran todas las transiciones descendentes entre niveles.
            ax: Ejes Matplotlib existentes. Si es None, se crea una figura nueva.

        Returns:
            tuple: Figura y ejes de Matplotlib, en ese orden.

        Raises:
            TypeError: Si n_max o los niveles de transición tienen tipos inválidos.
            ValueError: Si los niveles no son positivos, iguales o no están dibujados.
        """
        from .visualization import plot_energy_levels

        return plot_energy_levels(self, n_max=n_max, transitions=transitions, ax=ax)

    def plot_orbits(self, levels, ax=None):
        """Dibuja las órbitas circulares correspondientes a los niveles indicados.

        Args:
            levels: Iterable de números cuánticos principales positivos, sin duplicados.
            ax: Ejes Matplotlib existentes. Si es None, se crea una figura nueva.

        Returns:
            tuple: Figura y ejes de Matplotlib, en ese orden.

        Raises:
            TypeError: Si algún nivel no es entero.
            ValueError: Si no se proporcionan niveles o hay valores inválidos.
        """
        from .visualization import plot_orbits

        return plot_orbits(self, levels=levels, ax=ax)

    def plot_orbit_3d(
        self,
        n: int,
        phase: float = 0.0,
        inclination_deg: float = 25.0,
        elev: float = 25.0,
        azim: float = 45.0,
        show_velocity: bool = True,
        ax=None,
    ):
        """Dibuja la órbita relativa del sistema en un sistema de ejes 3D.

        Args:
            n: Número cuántico principal de la órbita.
            phase: Fase angular en radianes.
            inclination_deg: Inclinación del plano orbital en grados.
            elev: Elevación de la cámara 3D.
            azim: Azimut de la cámara 3D.
            show_velocity: Indica si se muestra la dirección de la velocidad.
            ax: Ejes 3D existentes o ``None`` para crear una figura nueva.

        Returns:
            tuple: Figura y ejes 3D de Matplotlib.

        Raises:
            ImportError: Si Matplotlib no está instalado.
            TypeError: Si los argumentos tienen tipos inválidos.
            ValueError: Si el nivel o los ángulos no son válidos.
        """
        from .visualization import plot_orbit_3d

        return plot_orbit_3d(
            self,
            n=n,
            phase=phase,
            inclination_deg=inclination_deg,
            elev=elev,
            azim=azim,
            show_velocity=show_velocity,
            ax=ax,
        )

    def animate_orbit_3d(self, n: int, **kwargs):
        """Crea una animación 3D de la rotación orbital del sistema.

        Args:
            n: Número cuántico principal de la órbita.
            **kwargs: Argumentos transferidos a
                ``bohr_atom.interactive.animate_orbit_3d``: frames, interval,
                revolutions, show_trail, inclination_deg, figsize,
                trail_length y orbit_points.

        Returns:
            matplotlib.animation.FuncAnimation: Animación 3D reproducible.

        Raises:
            ImportError: Si Matplotlib no está instalado.
            TypeError: Si los argumentos tienen tipos inválidos.
            ValueError: Si los parámetros no son válidos.
        """
        from .interactive import animate_orbit_3d

        return animate_orbit_3d(self, n=n, **kwargs)

    def interactive_orbit_3d_viewer(self, n_max: int = 6, **kwargs):
        """Crea un visor 3D con controles de fase, nivel y cámara en Jupyter.

        Args:
            n_max: Mayor número cuántico principal disponible.
            **kwargs: Argumentos transferidos a
                ``bohr_atom.interactive.interactive_orbit_3d_viewer`` como
                frames, interval, trail_length y orbit_points.

        Returns:
            ipywidgets.VBox: Panel de controles y lienzo Matplotlib 3D.

        Raises:
            ImportError: Si faltan ipywidgets o el backend ipympl.
            RuntimeError: Si no está activo el backend interactivo de ipympl.
            TypeError: Si los parámetros tienen tipos incorrectos.
            ValueError: Si los parámetros están fuera de sus dominios.
        """
        from .interactive import interactive_orbit_3d_viewer

        return interactive_orbit_3d_viewer(self, n_max=n_max, **kwargs)

    def animate_orbit(self, n: int, **kwargs):
        """Crea una animación Matplotlib de la coordenada relativa de la órbita n.

        La animación se reproduce a una velocidad visual y no al período físico
        real del sistema. Requiere las dependencias opcionales de visualización.

        Args:
            n: Número cuántico principal que se desea animar.
            **kwargs: Argumentos adicionales transferidos a
                bohr_atom.interactive.animate_orbit, como frames, interval,
                revolutions, show_trail, trail_length y figsize.

        Returns:
            matplotlib.animation.FuncAnimation: Animación de la órbita.

        Raises:
            ImportError: Si faltan dependencias opcionales de visualización.
            TypeError: Si los argumentos tienen tipos inválidos.
            ValueError: Si los parámetros están fuera de sus dominios permitidos.
        """
        from .interactive import animate_orbit

        return animate_orbit(self, n=n, **kwargs)

    def interactive_energy_diagram(self, max_n: int = 8):
        """Crea controles Jupyter para explorar niveles y transiciones electrónicas.

        Requiere instalar las dependencias opcionales mediante pip install -e
        ".[notebooks]".

        Args:
            max_n: Nivel principal máximo disponible en los controles.

        Returns:
            ipywidgets.VBox: Panel interactivo para visualizar niveles y transiciones.

        Raises:
            ImportError: Si no están instaladas las dependencias opcionales.
            ValueError: Si max_n no es un entero positivo.
        """
        from .interactive import interactive_energy_diagram

        return interactive_energy_diagram(self, max_n=max_n)

    def interactive_orbit_viewer(self, n_max: int = 6, **kwargs):
        """Crea un visor interactivo de órbitas para utilizar en Jupyter.

        Requiere instalar las dependencias opcionales mediante pip install -e
        ".[notebooks]".

        Args:
            n_max: Nivel principal máximo disponible en el selector.
            **kwargs: Argumentos adicionales transferidos a
                bohr_atom.interactive.interactive_orbit_viewer, como frames, interval, trail_length y orbit_points.

        Returns:
            ipywidgets.VBox: Panel para explorar la fase y la rotación orbital.

        Raises:
            ImportError: Si no están instaladas las dependencias opcionales.
            ValueError: Si los parámetros están fuera de sus dominios permitidos.
        """
        from .interactive import interactive_orbit_viewer

        return interactive_orbit_viewer(self, n_max=n_max, **kwargs)
