"""
Visualization tools for the Bohr model.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from .validation import validate_positive_integer


def plot_energy_levels(atom, n_max=5, transitions=None, ax=None):
    """
    Plot energy levels and electronic transitions.

    By default, all downward transitions between
    the displayed levels are represented.
    """

    n_max = validate_positive_integer(n_max, "n_max")

    energies = {n: atom.energy(n, unit="eV") for n in range(1, n_max + 1)}

    if transitions is None:
        transitions = [(ni, nf) for ni in range(2, n_max + 1) for nf in range(1, ni)]

    # Validate transitions

    for ni, nf in transitions:
        validate_positive_integer(ni, "initial level")

        validate_positive_integer(nf, "final level")

        if ni == nf or ni not in energies or nf not in energies:
            raise ValueError(
                "Transitions must connect different displayed energy levels."
            )

    if ax is None:
        fig, ax = plt.subplots(figsize=(11, 7))

    else:
        fig = ax.figure

    # Draw energy levels

    for n, energy in energies.items():
        ax.hlines(y=energy, xmin=0.1, xmax=0.65, linewidth=2)

        ax.text(0.68, energy, f"n={n}: {energy:.4f} eV", va="center")

    # Draw transitions

    for index, (ni, nf) in enumerate(transitions):
        Ei = energies[ni]

        Ef = energies[nf]

        x = 0.95 + index * 0.15

        ax.annotate(
            "",
            xy=(x, Ef),
            xytext=(x, Ei),
            arrowprops={"arrowstyle": "->", "linewidth": 1.3},
        )

        ax.text(x + 0.025, (Ei + Ef) / 2, f"{ni}→{nf}", fontsize=8, va="center")

    xmax = 1.2 + len(transitions) * 0.15

    ax.set_xlim(0, xmax)

    ax.set_ylabel("Energy (eV)")

    ax.set_title(f"Bohr energy levels - {atom.name}")

    ax.set_xticks([])

    ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()

    return fig, ax


def plot_orbits(atom, levels, ax=None):
    """
    Draw simplified circular Bohr orbits in the XY plane.

    Radii are expressed in picometers.
    """

    levels = list(levels)

    if not levels:
        raise ValueError("At least one level is required.")

    radii = {}

    for n in levels:
        n = validate_positive_integer(n, "n")

        radii[n] = atom.radius(n, unit="pm")

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))

    else:
        fig = ax.figure

    max_radius = max(radii.values())

    # Draw circular orbits

    for n, radius in radii.items():
        orbit = Circle(
            (0, 0), radius, fill=False, linewidth=1.6, label=f"n={n}: {radius:.2f} pm"
        )

        ax.add_patch(orbit)

        ax.annotate(f"n={n}", xy=(radius, 0), xytext=(5, 5), textcoords="offset points")

    # Draw nucleus

    ax.scatter([0], [0], s=65, marker="o", label="Nucleus", zorder=5)

    limit = max_radius * 1.2

    ax.set_xlim(-limit, limit)

    ax.set_ylim(-limit, limit)

    ax.set_aspect("equal")

    ax.set_xlabel("x (pm)")

    ax.set_ylabel("y (pm)")

    ax.set_title(f"Bohr orbits - {atom.name}")

    ax.grid(alpha=0.25)

    ax.legend()

    fig.tight_layout()

    return fig, ax
