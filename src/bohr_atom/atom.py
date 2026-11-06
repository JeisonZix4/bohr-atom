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
from .energy import energy_level_joule, reduced_mass
from .orbit import (
    convert_radius,
    orbital_angular_frequency_rad_s,
    orbital_period_s,
    orbital_radius_m,
)
from .transitions import transition_properties
from .validation import validate_positive_integer, validate_positive_real


class BohrAtom:
    """Representa un sistema de un electrón mediante el modelo de Bohr.

    Parameters
    ----------
    Z:
        Número atómico del núcleo; para un sistema hidrogenoide debe haber
        un único electrón y carga nuclear ``+Z e``.
    nucleus_mass_kg:
        Masa del núcleo en kilogramos.
    name:
        Etiqueta descriptiva utilizada en las representaciones gráficas.
    electron_mass_kg:
        Masa del electrón en kilogramos. Por defecto usa la constante CODATA.

    Notes
    -----
    Las fórmulas utilizan la masa reducida y describen la coordenada relativa
    electrón-núcleo. El modelo es no relativista y no incluye estructura fina,
    hiperfina ni efectos de tamaño nuclear.
    """

    def __init__(
        self,
        Z: int,
        nucleus_mass_kg: float,
        name: str = "Sistema hidrogenoide",
        electron_mass_kg: float = ELECTRON_MASS_KG,
    ) -> None:
        """Inicializa el sistema y calcula su masa reducida."""
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

        self.reduced_mass_kg = reduced_mass(
            self.electron_mass_kg,
            self.nucleus_mass_kg,
        )

    def __repr__(self) -> str:
        """Devuelve una representación breve y útil para depuración."""
        return (
            f"BohrAtom(name={self.name!r}, Z={self.Z}, "
            f"reduced_mass={self.reduced_mass_kg:.6e} kg)"
        )

    def energy(self, n: int, unit: str = "eV") -> float:
        """Calcula la energía del nivel principal ``n``.

        Parameters
        ----------
        n:
            Número cuántico principal positivo.
        unit:
            Unidad de salida: ``'J'`` para julios o ``'eV'`` para
            electronvoltios.

        Returns
        -------
        float
            Energía del estado ligado en la unidad solicitada.
        """
        energy_joule = energy_level_joule(
            n=n,
            Z=self.Z,
            mu=self.reduced_mass_kg,
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

        Parameters
        ----------
        n:
            Número cuántico principal positivo.
        unit:
            Unidad de salida: ``m``, ``nm``, ``pm`` o ``angstrom``.

        Returns
        -------
        float
            Radio o separación relativa en la unidad solicitada.
        """
        radius_m = orbital_radius_m(
            n=n,
            Z=self.Z,
            mu=self.reduced_mass_kg,
            elementary_charge_c=self.electron_charge_c,
            epsilon_0=self.epsilon_0,
            hbar=self.hbar,
        )
        return convert_radius(radius_m, unit)

    def orbital_angular_frequency(self, n: int) -> float:
        """Calcula la velocidad angular relativa de la órbita, en rad/s.

        No debe confundirse con la frecuencia del fotón emitido o absorbido
        durante una transición entre niveles.
        """
        return orbital_angular_frequency_rad_s(
            n=n,
            Z=self.Z,
            mu=self.reduced_mass_kg,
            elementary_charge_c=self.electron_charge_c,
            epsilon_0=self.epsilon_0,
            hbar=self.hbar,
        )

    def orbital_period(self, n: int) -> float:
        """Calcula el período de revolución relativo para el nivel ``n``.

        Returns
        -------
        float
            Período orbital en segundos.
        """
        return orbital_period_s(self.orbital_angular_frequency(n))

    def energy_levels(self, n_max: int = 5, energy_unit: str = "eV") -> list[dict]:
        """Genera una lista con energías y radios para los niveles 1 a ``n_max``.

        Parameters
        ----------
        n_max:
            Último número cuántico principal que se incluirá.
        energy_unit:
            Unidad de las energías: ``'J'`` o ``'eV'``.

        Returns
        -------
        list of dict
            Cada diccionario contiene ``n``, ``energy``, ``energy_unit`` y
            ``radius_pm``. Se devuelve una lista para no requerir Pandas en
            la biblioteca principal.
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
        """Calcula propiedades del fotón para una transición entre niveles.

        La variación de energía del átomo se define como ``E_final-E_inicial``.
        El resultado identifica emisión o absorción y devuelve energía del
        fotón, frecuencia y longitud de onda.
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
        """Representa niveles energéticos y transiciones con Matplotlib.

        Consulta :func:`bohr_atom.visualization.plot_energy_levels` para
        conocer los parámetros y el formato de retorno.
        """
        from .visualization import plot_energy_levels

        return plot_energy_levels(self, n_max=n_max, transitions=transitions, ax=ax)

    def plot_orbits(self, levels, ax=None):
        """Dibuja órbitas circulares para los niveles indicados.

        Consulta :func:`bohr_atom.visualization.plot_orbits` para conocer
        las unidades y las convenciones de la representación.
        """
        from .visualization import plot_orbits

        return plot_orbits(self, levels=levels, ax=ax)

    def animate_orbit(self, n: int, **kwargs):
        """Crea una animación Matplotlib de la órbita relativa del nivel ``n``.

        Este método requiere las dependencias opcionales de visualización
        interactiva. La animación se reproduce a una velocidad visual,
        no al período físico real del sistema.
        """
        from .interactive import animate_orbit

        return animate_orbit(self, n=n, **kwargs)

    def interactive_energy_diagram(self, max_n: int = 8):
        """Crea controles Jupyter para explorar niveles y transiciones.

        Requiere instalar las dependencias opcionales ``.[notebooks]``.
        """
        from .interactive import interactive_energy_diagram

        return interactive_energy_diagram(self, max_n=max_n)

    def interactive_orbit_viewer(self, n_max: int = 6, **kwargs):
        """Crea un visor interactivo de órbitas para usar en Jupyter.

        Requiere instalar las dependencias opcionales ``.[notebooks]``.
        """
        from .interactive import interactive_orbit_viewer

        return interactive_orbit_viewer(self, n_max=n_max, **kwargs)
