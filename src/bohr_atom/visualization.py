"""Gráficos estáticos para los niveles y las órbitas del modelo de Bohr.

Matplotlib se importa dentro de las funciones para mantener explícito que
los gráficos son una capa de presentación y no parte de los cálculos base.
"""

from .validation import validate_positive_integer


def plot_energy_levels(atom, n_max: int = 5, transitions=None, ax=None):
    """Dibuja niveles energéticos y flechas de transición descendentes.

    Parameters
    ----------
    atom:
        Instancia de :class:`bohr_atom.BohrAtom`.
    n_max:
        Último nivel principal que se dibujará.
    transitions:
        Iterable opcional de pares ``(n_inicial, n_final)``. Si se omite,
        se representan todas las transiciones descendentes entre los
        niveles mostrados.
    ax:
        Ejes de Matplotlib existentes. Si es ``None``, se crean una figura
        y unos ejes nuevos.

    Returns
    -------
    tuple
        Objetos ``(fig, ax)`` de Matplotlib.
    """
    import matplotlib.pyplot as plt

    n_max = validate_positive_integer(n_max, "n_max")
    energies = {n: atom.energy(n, unit="eV") for n in range(1, n_max + 1)}

    if transitions is None:
        transitions = [
            (n_initial, n_final)
            for n_initial in range(2, n_max + 1)
            for n_final in range(1, n_initial)
        ]
    else:
        transitions = list(transitions)

    # Validar todos los pares antes de dibujar para evitar gráficos parciales.
    for pair in transitions:
        if len(pair) != 2:
            raise ValueError(
                "Cada transición debe ser un par (n_inicial, n_final)."
            )
        n_initial = validate_positive_integer(pair[0], "n_initial")
        n_final = validate_positive_integer(pair[1], "n_final")
        if (
            n_initial == n_final
            or n_initial not in energies
            or n_final not in energies
        ):
            raise ValueError(
                "Las transiciones deben conectar niveles distintos dibujados."
            )

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.figure

    # Cada estado se representa por un segmento horizontal a su energía.
    for n, energy in energies.items():
        ax.hlines(energy, 0.08, 0.58, linewidth=2.0)
        ax.text(0.61, energy, f"n={n}: {energy:.5f} eV", va="center", fontsize=9)

    # La flecha sigue el sentido del cambio del estado inicial al final;
    # flechas hacia abajo representan emisión y hacia arriba absorción.
    for index, (n_initial, n_final) in enumerate(transitions):
        energy_initial = energies[n_initial]
        energy_final = energies[n_final]
        x_position = 0.88 + 0.16 * index
        ax.annotate(
            "",
            xy=(x_position, energy_final),
            xytext=(x_position, energy_initial),
            arrowprops={"arrowstyle": "-|>", "linewidth": 1.35},
        )
        ax.text(
            x_position + 0.02,
            0.5 * (energy_initial + energy_final),
            f"{n_initial}→{n_final}",
            fontsize=8,
            va="center",
        )

    ax.axhline(0.0, linestyle="--", linewidth=1.0, alpha=0.7)
    ax.text(0.02, 0.0, " E = 0 (ionización)", va="bottom", fontsize=8)
    ax.set_xlim(0.0, max(1.2, 1.1 + 0.16 * len(transitions)))
    ax.set_ylabel("Energía (eV)")
    ax.set_title(f"Niveles energéticos de {atom.name}")
    ax.set_xticks([])
    ax.grid(axis="y", alpha=0.22)
    fig.tight_layout()
    return fig, ax


def plot_orbits(atom, levels, ax=None):
    """Representa órbitas circulares concéntricas en el plano ``xy``.

    Los radios mostrados son las separaciones relativas electrón-núcleo,
    expresadas en picómetros. La figura es una representación del modelo
    de Bohr y no una representación de orbitales cuánticos.

    Parameters
    ----------
    atom:
        Instancia de :class:`bohr_atom.BohrAtom`.
    levels:
        Iterable de números cuánticos que se desean representar.
    ax:
        Ejes de Matplotlib existentes o ``None`` para crear una figura.

    Returns
    -------
    tuple
        Objetos ``(fig, ax)`` de Matplotlib.
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    level_values = [validate_positive_integer(n, "level") for n in levels]
    if not level_values:
        raise ValueError("Debe proporcionarse al menos un nivel orbital.")
    if len(set(level_values)) != len(level_values):
        raise ValueError("La lista de niveles no debe contener duplicados.")

    radii = {n: atom.radius(n, unit="pm") for n in level_values}
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 7))
    else:
        fig = ax.figure

    for n, radius in radii.items():
        # Cada circunferencia indica el radio permitido para ese n.
        ax.add_patch(
            Circle(
                (0.0, 0.0),
                radius,
                fill=False,
                linewidth=1.6,
                label=f"n={n}: {radius:.3f} pm",
            )
        )
        ax.annotate(
            f"n={n}",
            xy=(radius, 0.0),
            xytext=(4, 5),
            textcoords="offset points",
        )

    ax.scatter([0.0], [0.0], s=65, marker="o", label="Núcleo (origen)", zorder=5)
    limit = max(radii.values()) * 1.2
    ax.set(xlim=(-limit, limit), ylim=(-limit, limit))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (pm)")
    ax.set_ylabel("y (pm)")
    ax.set_title(f"Órbitas de Bohr — {atom.name}")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    return fig, ax
