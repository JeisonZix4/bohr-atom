"""Widgets y animaciones para explorar visualmente el modelo de Bohr.

Este módulo es opcional: las dependencias de Jupyter se importan dentro de
las funciones que las necesitan. Así, los cálculos físicos básicos pueden
utilizarse sin instalar ``ipywidgets`` ni ``IPython``.

Las animaciones representan la coordenada relativa electrón-núcleo. Su
reproducción está acelerada y no representa el tiempo atómico en tiempo real.
"""

from math import isfinite, pi
from numbers import Integral, Real

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle


def _validate_frames(frames: int) -> int:
    """Valida la cantidad de fotogramas de una animación.

    Args:
        frames: Cantidad de fotogramas. Debe ser un entero mayor o igual que dos.

    Returns:
        int: Cantidad de fotogramas validada.

    Raises:
        TypeError: Si frames no es un entero o es un booleano.
        ValueError: Si frames es menor que dos.
    """
    if isinstance(frames, bool) or not isinstance(frames, Integral):
        raise TypeError("frames debe ser un número entero.")
    if frames < 2:
        raise ValueError("frames debe ser mayor o igual que 2.")
    return int(frames)


def _validate_interval(interval: float) -> float:
    """Valida el intervalo visual entre fotogramas.

    Args:
        interval: Tiempo entre fotogramas en milisegundos. Debe ser finito y positivo.

    Returns:
        float: Intervalo visual convertido a float, en milisegundos.

    Raises:
        TypeError: Si interval no es un número real o es un booleano.
        ValueError: Si interval no es finito o no es positivo.
    """
    if isinstance(interval, bool) or not isinstance(interval, Real):
        raise TypeError("interval debe ser un número real.")
    value = float(interval)
    if not isfinite(value) or value <= 0.0:
        raise ValueError("interval debe ser finito y positivo.")
    return value


def animate_orbit(
    atom,
    n: int,
    frames: int = 180,
    interval: float = 30,
    revolutions: float = 1.0,
    show_trail: bool = True,
    figsize: tuple[float, float] = (6.5, 6.5),
) -> FuncAnimation:
    """Construye una animación de la coordenada relativa de la órbita.

    Args:
        atom: Instancia de :class:`bohr_atom.BohrAtom`.
        n: Número cuántico principal de la órbita que se representará.
        frames: Número de fotogramas de la animación.
        interval: Tiempo de espera visual entre fotogramas, en milisegundos.
        revolutions: Número de vueltas representadas en un ciclo de animación.
        show_trail: Si es ``True``, muestra el tramo de trayectoria ya recorrido.
        figsize: Tamaño de la figura de Matplotlib.

    Returns:
        matplotlib.animation.FuncAnimation: Objeto de animación. En Jupyter puede
            mostrarse mediante ``IPython.display.HTML(animation.to_jshtml())``.

    Note:
        El intervalo visual no es el período físico. El período calculado se
        muestra como dato numérico porque los tiempos orbitales son demasiado
        pequeños para reproducirse directamente en una pantalla.
    """
    from .validation import validate_positive_integer, validate_positive_real

    n = validate_positive_integer(n, "n")
    frames = _validate_frames(frames)
    interval = _validate_interval(interval)
    revolutions = validate_positive_real(revolutions, "revolutions")

    radius_pm = atom.radius(n, unit="pm")
    omega = atom.orbital_angular_frequency(n)
    period = atom.orbital_period(n)

    fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
    ax.add_patch(
        Circle(
            (0.0, 0.0), radius_pm, fill=False, linewidth=1.8,
            linestyle="--", alpha=0.8, label=f"Órbita n={n}",
        )
    )
    # En la coordenada relativa el origen se coloca en el núcleo y el vector
    # dibujado representa la separación r = r_e - r_N. No se dibuja por
    # separado el movimiento del núcleo alrededor del centro de masa.
    ax.scatter([0.0], [0.0], s=100, marker="o", zorder=5, label="Núcleo (origen)")
    trail_line, = ax.plot([], [], linewidth=2.0, alpha=0.75, label="Trayectoria")
    electron, = ax.plot(
        [], [], marker="o", linestyle="None", markersize=11,
        markeredgewidth=1.2, label="Electrón",
    )
    tangent = ax.annotate(
        "", xy=(0.0, 0.0), xytext=(0.0, 0.0),
        arrowprops={"arrowstyle": "->", "linewidth": 1.6},
    )

    limit = radius_pm * 1.28
    ax.set(xlim=(-limit, limit), ylim=(-limit, limit))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (pm)")
    ax.set_ylabel("y (pm)")
    ax.set_title(f"Rotación ilustrativa — {atom.name}, n={n}")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right")
    ax.text(
        0.02, 0.02,
        f"r = {radius_pm:.4f} pm\nω = {omega:.4e} rad/s\nT = {period:.4e} s",
        transform=ax.transAxes, va="bottom", ha="left", fontsize=9,
        bbox={"boxstyle": "round,pad=0.4", "alpha": 0.12},
    )

    def initialize_animation():
        """Inicializa los artistas gráficos antes del primer fotograma.

        Returns:
            tuple: Artistas de Matplotlib que se actualizarán durante la animación.
        """
        electron.set_data([], [])
        trail_line.set_data([], [])
        tangent.xy = (0.0, 0.0)
        tangent.set_position((0.0, 0.0))
        return electron, trail_line, tangent

    def update_animation(frame: int):
        """Actualiza la posición, la trayectoria y la tangente del electrón.

        Args:
            frame: Índice del fotograma actual, dentro del intervalo definido para
                la animación.

        Returns:
            tuple: Artistas de Matplotlib modificados en el fotograma actual.
        """
        theta = 2.0 * pi * revolutions * frame / (frames - 1)
        x_position = radius_pm * np.cos(theta)
        y_position = radius_pm * np.sin(theta)
        electron.set_data([x_position], [y_position])

        if show_trail:
            phases = np.linspace(0.0, theta, max(2, frame + 1))
            trail_line.set_data(radius_pm * np.cos(phases), radius_pm * np.sin(phases))
        else:
            trail_line.set_data([], [])

        # El vector tangente indica el sentido instantáneo del movimiento.
        tangent_length = 0.20 * radius_pm
        tangent.xy = (
            x_position - tangent_length * np.sin(theta),
            y_position + tangent_length * np.cos(theta),
        )
        tangent.set_position((x_position, y_position))
        return electron, trail_line, tangent

    return FuncAnimation(
        fig,
        update_animation,
        frames=frames,
        init_func=initialize_animation,
        interval=interval,
        blit=False,
        repeat=True,
        cache_frame_data=False,
    )


def interactive_energy_diagram(atom, max_n: int = 8):
    """Crea un panel ipywidgets para explorar una transición electrónica.

    El usuario puede seleccionar el número máximo de niveles y los estados
    inicial y final. El panel muestra el diagrama y las propiedades del fotón.

    Args:
        atom: Instancia de bohr_atom.BohrAtom que proporciona las energías.
        max_n: Límite superior permitido para los selectores de nivel.

    Returns:
        ipywidgets.VBox: Panel interactivo compatible con JupyterLab.

    Raises:
        ImportError: Si no están instaladas las dependencias opcionales de notebooks.
        TypeError: Si max_n no es un entero.
        ValueError: Si max_n es menor que dos.
    """
    try:
        import ipywidgets as widgets
    except ImportError as exc:
        raise ImportError(
            "Esta función requiere ipywidgets e IPython. Instala con: "
            'python -m pip install -e ".[notebooks]"'
        ) from exc

    from .validation import validate_positive_integer

    max_n = validate_positive_integer(max_n, "max_n")
    if max_n < 2:
        raise ValueError("max_n debe ser al menos 2.")

    n_max_widget = widgets.IntSlider(
        value=min(6, max_n), min=2, max=max_n, step=1,
        description="Niveles:", continuous_update=False,
        style={"description_width": "initial"},
    )
    n_initial_widget = widgets.IntSlider(
        value=min(3, max_n), min=1, max=max_n, step=1,
        description="Nivel inicial:", continuous_update=False,
        style={"description_width": "initial"},
    )
    n_final_widget = widgets.IntSlider(
        value=min(2, max_n), min=1, max=max_n, step=1,
        description="Nivel final:", continuous_update=False,
        style={"description_width": "initial"},
    )

    output = widgets.interactive_output(
        _render_energy_diagram,
        {
            "atom": widgets.fixed(atom),
            "n_max": n_max_widget,
            "n_initial": n_initial_widget,
            "n_final": n_final_widget,
        },
    )
    controls = widgets.VBox(
        [
            widgets.HTML("<h3>Explorador de niveles energéticos</h3>"),
            n_max_widget,
            n_initial_widget,
            n_final_widget,
        ]
    )
    return widgets.VBox([controls, output])


def _render_energy_diagram(atom, n_max, n_initial, n_final):
    """Dibuja la transición seleccionada y presenta sus datos fotónicos.

    Args:
        atom: Instancia de BohrAtom utilizada para calcular energías y fotones.
        n_max: Número cuántico máximo que se representa en el diagrama.
        n_initial: Nivel cuántico inicial de la transición.
        n_final: Nivel cuántico final de la transición.

    Returns:
        None: Muestra el gráfico y la información mediante la salida de IPython.
    """
    from IPython.display import display

    if n_initial == n_final:
        print("Selecciona dos niveles diferentes.")
        return
    if n_initial > n_max or n_final > n_max:
        print("Los niveles inicial y final deben estar dentro del diagrama.")
        return

    transition = atom.transition(n_initial, n_final)
    process_label = "emisión" if transition["process"] == "emission" else "absorción"
    energies = {n: atom.energy(n, unit="eV") for n in range(1, n_max + 1)}
    fig, ax = plt.subplots(figsize=(9.0, 5.8), constrained_layout=True)

    for level, energy in energies.items():
        highlighted = level in {n_initial, n_final}
        ax.hlines(
            energy, 0.08, 0.55,
            linewidth=2.8 if highlighted else 1.5,
            alpha=1.0 if highlighted else 0.65,
        )
        ax.text(0.055, energy, f"n={level}", ha="right", va="center", fontsize=9)
        ax.text(0.58, energy, f"{energy:.5f} eV", ha="left", va="center", fontsize=9)

    # El cero de energía representa el límite de ionización del sistema.
    ax.axhline(0.0, linestyle=":", linewidth=1.4, alpha=0.8)
    ax.text(
        0.50, 0.0, "Límite de ionización (E = 0)",
        ha="center", va="bottom", fontsize=9,
    )
    ax.annotate(
        "",
        xy=(0.82, energies[n_final]),
        xytext=(0.82, energies[n_initial]),
        arrowprops={"arrowstyle": "-|>", "linewidth": 2.3},
    )
    midpoint = 0.5 * (energies[n_initial] + energies[n_final])
    ax.text(
        0.85, midpoint,
        f"{n_initial} → {n_final}\n{process_label}",
        ha="left", va="center", fontsize=10,
    )

    lower = min(energies.values())
    ax.set_ylim(lower * 1.12, max(0.8, 0.12 * abs(lower)))
    ax.set_xlim(-0.08, 1.18)
    ax.set_xticks([])
    ax.set_ylabel("Energía (eV)")
    ax.set_title(f"Niveles energéticos de {atom.name}")
    ax.grid(axis="y", alpha=0.22)
    ax.text(
        0.98, 0.03,
        f"Eγ = {transition['photon_energy_ev']:.6f} eV\n"
        f"ν = {transition['frequency_hz']:.4e} Hz\n"
        f"λ = {transition['wavelength_nm']:.4f} nm",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=9,
        bbox={"boxstyle": "round,pad=0.5", "alpha": 0.12},
    )
    display(fig)
    plt.close(fig)


def interactive_orbit_viewer(
    atom, n_max: int = 6, frames: int = 180, interval: float = 35
):
    """Crea un visor orbital con selector de nivel, fase y reproducción.

    Args:
        atom: Instancia de BohrAtom que define el sistema hidrogenoide.
        n_max: Mayor número cuántico principal disponible en el selector.
        frames: Cantidad de posiciones angulares de la animación.
        interval: Intervalo visual entre posiciones, en milisegundos.

    Returns:
        ipywidgets.VBox: Panel interactivo compatible con JupyterLab.

    Raises:
        ImportError: Si no están instaladas ipywidgets e IPython.
        TypeError: Si los parámetros tienen tipos inválidos.
        ValueError: Si los valores están fuera de sus dominios permitidos.
    """
    try:
        import ipywidgets as widgets
    except ImportError as exc:
        raise ImportError(
            "Esta función requiere ipywidgets e IPython. Instala con: "
            'python -m pip install -e ".[notebooks]"'
        ) from exc

    from .validation import validate_positive_integer

    n_max = validate_positive_integer(n_max, "n_max")
    frames = _validate_frames(frames)
    interval = _validate_interval(interval)

    n_widget = widgets.IntSlider(
        value=min(2, n_max), min=1, max=n_max, step=1,
        description="Nivel n:", continuous_update=False,
        style={"description_width": "initial"},
    )
    phase_widget = widgets.IntSlider(
        value=0, min=0, max=frames - 1, step=1,
        description="Fase:", continuous_update=True,
        style={"description_width": "initial"},
        layout=widgets.Layout(width="70%"),
    )
    play_widget = widgets.Play(
        value=0, min=0, max=frames - 1, step=1,
        interval=int(interval), description="Reproducir",
    )
    # Vincular Play y el deslizador permite pausar y elegir una fase manualmente.
    widgets.jslink((play_widget, "value"), (phase_widget, "value"))
    trail_widget = widgets.Checkbox(
        value=True, description="Mostrar trayectoria", indent=False
    )

    output = widgets.interactive_output(
        _render_orbit_frame,
        {
            "atom": widgets.fixed(atom),
            "n": n_widget,
            "frame": phase_widget,
            "frames": widgets.fixed(frames),
            "show_trail": trail_widget,
        },
    )
    controls = widgets.VBox(
        [
            widgets.HTML("<h3>Visor interactivo de órbitas</h3>"),
            n_widget,
            widgets.HBox([play_widget, phase_widget]),
            trail_widget,
        ]
    )
    return widgets.VBox([controls, output])


def _render_orbit_frame(atom, n, frame, frames, show_trail):
    """Actualiza la posición del electrón para el nivel y ángulo seleccionados.

    Args:
        atom: Instancia de BohrAtom que proporciona el radio orbital.
        n: Número cuántico principal de la órbita representada.
        frame: Índice de la posición angular actual.
        frames: Número total de posiciones disponibles.
        show_trail: Indica si se dibuja la trayectoria recorrida.

    Returns:
        None: Actualiza la salida gráfica de Jupyter.
    """
    from IPython.display import display

    radius_pm = atom.radius(n, unit="pm")
    angular_frequency = atom.orbital_angular_frequency(n)
    period = atom.orbital_period(n)
    theta = 2.0 * pi * frame / (frames - 1)
    x_position = radius_pm * np.cos(theta)
    y_position = radius_pm * np.sin(theta)

    fig, ax = plt.subplots(figsize=(6.2, 6.2), constrained_layout=True)
    ax.add_patch(
        Circle(
            (0.0, 0.0), radius_pm, fill=False,
            linestyle="--", linewidth=1.8,
        )
    )
    ax.scatter([0.0], [0.0], s=100, marker="o", label="Núcleo (origen)", zorder=4)

    if show_trail and frame > 0:
        phases = np.linspace(0.0, theta, frame + 1)
        ax.plot(
            radius_pm * np.cos(phases),
            radius_pm * np.sin(phases),
            linewidth=2.0,
            label="Trayectoria recorrida",
        )

    ax.scatter(
        [x_position], [y_position], s=125, marker="o",
        label="Electrón", zorder=5,
    )
    tangent_length = 0.20 * radius_pm
    ax.annotate(
        "",
        xy=(
            x_position - tangent_length * np.sin(theta),
            y_position + tangent_length * np.cos(theta),
        ),
        xytext=(x_position, y_position),
        arrowprops={"arrowstyle": "->", "linewidth": 1.6},
    )

    limit = radius_pm * 1.3
    ax.set(xlim=(-limit, limit), ylim=(-limit, limit))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (pm)")
    ax.set_ylabel("y (pm)")
    ax.set_title(f"{atom.name} — órbita de Bohr, n={n}")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right")
    ax.text(
        0.03,
        0.03,
        f"θ = {np.degrees(theta):.1f}°\nr = {radius_pm:.4f} pm\n"
        f"ω = {angular_frequency:.3e} rad/s\nT = {period:.3e} s",
        transform=ax.transAxes, va="bottom",
        bbox={"boxstyle": "round,pad=0.4", "alpha": 0.12},
    )
    display(fig)
    plt.close(fig)
