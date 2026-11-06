"""Gráficos estáticos para los niveles y las órbitas del modelo de Bohr.

Matplotlib se importa dentro de las funciones para mantener explícito que
los gráficos son una capa de presentación y no parte de los cálculos base.
"""

from .validation import validate_positive_integer


def plot_energy_levels(atom, n_max: int = 5, transitions=None, ax=None):
    """Dibuja niveles energéticos y flechas de transición descendentes.

    Args:
        atom: Instancia de :class:`bohr_atom.BohrAtom`.
        n_max: Último nivel principal que se dibujará.
        transitions: Iterable opcional de pares ``(n_inicial, n_final)``. Si se
            omite, se representan todas las transiciones descendentes entre
            los niveles mostrados.
        ax: Ejes de Matplotlib existentes. Si es ``None``, se crea una figura
            con sus ejes.

    Returns:
        tuple: Objetos ``(fig, ax)`` de Matplotlib.
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

    Args:
        atom: Instancia de :class:`bohr_atom.BohrAtom`.
        levels: Iterable de números cuánticos que se desean representar.
        ax: Ejes de Matplotlib existentes o ``None`` para crear una figura.

    Returns:
        tuple: Objetos ``(fig, ax)`` de Matplotlib.
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



def plot_orbit_3d(
    atom,
    n: int,
    phase: float = 0.0,
    inclination_deg: float = 25.0,
    elev: float = 25.0,
    azim: float = 45.0,
    show_velocity: bool = True,
    ax=None,
):
    """Representa en tres dimensiones la órbita relativa del electrón.

    La órbita de Bohr es circular y plana; su orientación se expresa mediante
    ``inclination_deg`` para visualizar el plano orbital en un sistema 3D. El
    origen representa el núcleo en la coordenada relativa electrón-núcleo.
    El vector tangente indica el sentido instantáneo de rotación.

    Args:
        atom: Instancia de ``BohrAtom`` que proporciona las magnitudes físicas.
        n: Número cuántico principal positivo de la órbita.
        phase: Fase angular inicial en radianes.
        inclination_deg: Inclinación del plano orbital respecto del plano xy,
            expresada en grados.
        elev: Ángulo de elevación de la cámara de Matplotlib, en grados.
        azim: Ángulo azimutal de la cámara de Matplotlib, en grados.
        show_velocity: Si es ``True``, dibuja el vector tangente de velocidad.
        ax: Ejes 3D existentes. Si es ``None``, crea una figura nueva.

    Returns:
        tuple: Figura y ejes 3D de Matplotlib, en ese orden.

    Raises:
        TypeError: Si ``n`` o los ángulos no tienen tipos numéricos válidos.
        ValueError: Si los ángulos no son finitos o la inclinación está fuera
            del intervalo permitido entre 0 y 180 grados.

    Note:
        El radio corresponde a la separación relativa electrón-núcleo. La
        magnitud ``v_rel = omega * r`` es la rapidez de la coordenada relativa,
        no la rapidez visual de reproducción. La representación no es un
        orbital cuántico ni una trayectoria de la mecánica cuántica moderna.
    """
    from math import isfinite, pi
    from numbers import Real

    import numpy as np
    import matplotlib.pyplot as plt
    from .validation import validate_positive_integer

    n = validate_positive_integer(n, "n")
    for value, label in (
        (phase, "phase"),
        (inclination_deg, "inclination_deg"),
        (elev, "elev"),
        (azim, "azim"),
    ):
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError(f"{label} debe ser un número real.")
        if not isfinite(float(value)):
            raise ValueError(f"{label} debe ser finito.")
    if not 0.0 <= float(inclination_deg) <= 180.0:
        raise ValueError("inclination_deg debe estar entre 0 y 180 grados.")

    radius_pm = atom.radius(n, unit="pm")
    radius_m = atom.radius(n, unit="m")
    omega = atom.orbital_angular_frequency(n)
    relative_speed = omega * radius_m
    inclination = np.deg2rad(float(inclination_deg))
    theta = float(phase)

    # Parametrizar una circunferencia y rotar su plano alrededor del eje x.
    angles = np.linspace(0.0, 2.0 * pi, 361)
    orbit_x = radius_pm * np.cos(angles)
    orbit_y = radius_pm * np.sin(angles) * np.cos(inclination)
    orbit_z = radius_pm * np.sin(angles) * np.sin(inclination)

    x = radius_pm * np.cos(theta)
    y = radius_pm * np.sin(theta) * np.cos(inclination)
    z = radius_pm * np.sin(theta) * np.sin(inclination)

    if ax is None:
        fig = plt.figure(figsize=(8.5, 7.0), constrained_layout=True)
        ax = fig.add_subplot(111, projection="3d")
    else:
        if not hasattr(ax, "get_zlim"):
            raise TypeError("ax debe ser un conjunto de ejes 3D de Matplotlib.")
        fig = ax.figure

    ax.plot(
        orbit_x, orbit_y, orbit_z,
        linestyle="--", linewidth=1.7, alpha=0.75,
        label=f"Órbita permitida (n={n})",
    )
    ax.scatter([0.0], [0.0], [0.0], s=110, marker="o", label="Núcleo", zorder=5)
    ax.scatter([x], [y], [z], s=75, marker="o", label="Electrón", zorder=6)

    # El vector tangente tiene dirección proporcional a dr/dtheta.
    if show_velocity:
        tangent_x = -np.sin(theta)
        tangent_y = np.cos(theta) * np.cos(inclination)
        tangent_z = np.cos(theta) * np.sin(inclination)
        ax.quiver(
            x, y, z,
            tangent_x, tangent_y, tangent_z,
            length=0.24 * radius_pm,
            normalize=True,
            color="tab:green",
            arrow_length_ratio=0.28,
            linewidth=2.0,
            label="Dirección de la velocidad",
        )

    limit = 1.25 * radius_pm
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=float(elev), azim=float(azim))
    ax.set_xlabel("x (pm)")
    ax.set_ylabel("y (pm)")
    ax.set_zlabel("z (pm)")
    ax.set_title(f"Órbita 3D de {atom.name} — Z={atom.Z}, n={n}")
    ax.legend(loc="upper right")
    ax.text2D(
        0.02, 0.96,
        f"r = {radius_pm:.5g} pm\n"
        f"ω = {omega:.4e} rad/s\n"
        f"v_rel = {relative_speed:.4e} m/s\n"
        f"T = {atom.orbital_period(n):.4e} s",
        transform=ax.transAxes,
        va="top",
        bbox={"boxstyle": "round,pad=0.4", "alpha": 0.12},
    )
    return fig, ax
