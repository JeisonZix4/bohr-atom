"""
BohrAtom class.
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
from .orbit import convert_radius, orbital_radius_m
from .transitions import transition_properties
from .validation import validate_positive_integer, validate_positive_real


class BohrAtom:
    """
    Hydrogen-like atom using the Bohr model.
    """

    def __init__(
        self,
        Z,
        nucleus_mass_kg,
        name="Hydrogen-like atom",
        electron_mass_kg=ELECTRON_MASS_KG,
    ):

        self.Z = validate_positive_integer(Z, "Z")

        self.nucleus_mass_kg = validate_positive_real(
            nucleus_mass_kg, "nucleus_mass_kg"
        )

        self.electron_mass_kg = validate_positive_real(
            electron_mass_kg, "electron_mass_kg"
        )

        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string.")

        self.name = name

        # Electric charges

        self.electron_charge_c = -ELEMENTARY_CHARGE_C

        self.nuclear_charge_c = self.Z * ELEMENTARY_CHARGE_C

        # Physical constants

        self.epsilon_0 = VACUUM_PERMITTIVITY_F_M

        self.planck_constant = PLANCK_CONSTANT_J_S

        self.hbar = REDUCED_PLANCK_CONSTANT_J_S

        self.speed_of_light = SPEED_OF_LIGHT_M_S

        # Reduced mass

        self.reduced_mass_kg = reduced_mass(self.electron_mass_kg, self.nucleus_mass_kg)

    def __repr__(self):

        return (
            f"BohrAtom(name='{self.name}', "
            f"Z={self.Z}, "
            f"reduced_mass={self.reduced_mass_kg:.5e} kg)"
        )

    def energy(self, n, unit="eV"):
        """
        Calculate the energy of level n.
        """

        energy_j = energy_level_joule(
            n=n,
            Z=self.Z,
            mu=self.reduced_mass_kg,
            elementary_charge_c=self.electron_charge_c,
            epsilon_0=self.epsilon_0,
            hbar=self.hbar,
        )

        unit = unit.lower()

        if unit == "j":
            return energy_j

        if unit == "ev":
            return energy_j / ELEMENTARY_CHARGE_C

        raise ValueError("Energy unit must be 'J' or 'eV'.")

    def radius(self, n, unit="m"):
        """
        Calculate the Bohr orbital radius.
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

    def energy_levels(self, n_max=5, energy_unit="eV"):
        """
        Generate a table-like list of energy levels.
        """

        n_max = validate_positive_integer(n_max, "n_max")

        results = []

        for n in range(1, n_max + 1):
            results.append(
                {
                    "n": n,
                    "energy": self.energy(n, unit=energy_unit),
                    "energy_unit": energy_unit,
                    "radius_pm": self.radius(n, unit="pm"),
                }
            )

        return results

    def transition(self, n_initial, n_final):
        """
        Calculate an electronic transition.
        """

        E_initial = self.energy(n_initial, unit="J")

        E_final = self.energy(n_final, unit="J")

        return transition_properties(
            n_initial=n_initial,
            n_final=n_final,
            energy_initial_j=E_initial,
            energy_final_j=E_final,
            h=self.planck_constant,
            c=self.speed_of_light,
            elementary_charge_c=ELEMENTARY_CHARGE_C,
        )

    def plot_energy_levels(self, n_max=5, transitions=None, ax=None):

        from .visualization import plot_energy_levels

        return plot_energy_levels(
            atom=self, n_max=n_max, transitions=transitions, ax=ax
        )

    def plot_orbits(self, levels, ax=None):

        from .visualization import plot_orbits

        return plot_orbits(atom=self, levels=levels, ax=ax)
