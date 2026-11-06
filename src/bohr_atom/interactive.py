"""Widgets y animaciones para explorar visualmente el modelo de Bohr.

Este módulo forma parte de las dependencias opcionales de Jupyter. Los widgets
permiten modificar niveles, transiciones, fase y velocidad de reproducción.
Las animaciones muestran la coordenada relativa electrón-núcleo y utilizan
un tiempo visual acelerado, no el período atómico como tiempo de pantalla.
"""

from math import isfinite, pi
from numbers import Integral, Real

import matplotlib
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
        TypeError: Si ``frames`` no es entero o es un booleano.
        ValueError: Si ``frames`` es menor que dos.
    """
    if isinstance(frames, bool) or not isinstance(frames, Integral):
        raise TypeError("frames debe ser un número entero.")
    if frames < 2:
        raise ValueError("frames debe ser mayor o igual que 2.")
    return int(frames)


def _validate_interval(interval: float) -> float:
    """Valida el intervalo visual entre fotogramas.

    Args:
        interval: Tiempo entre fotogramas en milisegundos.

    Returns:
        float: Intervalo visual finito y positivo, en milisegundos.

    Raises:
        TypeError: Si ``interval`` no es un número real o es un booleano.
        ValueError: Si ``interval`` no es finito o no es positivo.
    """
    if isinstance(interval, bool) or not isinstance(interval, Real):
        raise TypeError("interval debe ser un número real.")
    value = float(interval)
    if not isfinite(value) or value <= 0.0:
        raise ValueError("interval debe ser finito y positivo.")
    return value


def _import_widgets():
    """Importa ipywidgets o comunica cómo instalar las dependencias opcionales.

    Returns:
        module: Módulo ``ipywidgets``.

    Raises:
        ImportError: Si no está instalado el extra de dependencias para notebooks.
    """
    try:
        import ipywidgets as widgets
    except ImportError as exc:
        raise ImportError(
            "Esta funcionalidad requiere las dependencias interactivas. "
            'Instala con: python -m pip install -e ".[notebooks]"'
        ) from exc
    return widgets


def _require_widget_backend() -> None:
    """Comprueba que Matplotlib utiliza el backend interactivo de ipympl.

    Raises:
        RuntimeError: Si el backend activo no es el backend de widgets.
    """
    backend = str(matplotlib.get_backend()).lower()
    if "ipympl" not in backend and "widget" not in backend:
        raise RuntimeError(
            "El visor orbital necesita el backend interactivo de ipympl. "
            "En una celda de Jupyter ejecuta `%matplotlib widget` antes de "
            "importar bohr_atom.interactive y vuelve a ejecutar el notebook."
        )


def _phase_coordinates(radius: float, phase: float) -> tuple[float, float]:
    """Calcula las coordenadas cartesianas para un radio y ángulo dados.

    Args:
        radius: Radio de la órbita en la unidad que utilice el gráfico.
        phase: Ángulo en radianes.

    Returns:
        tuple[float, float]: Coordenadas ``(x, y)`` de la posición relativa.
    """
    return radius * np.cos(phase), radius * np.sin(phase)


def animate_orbit(
    atom,
    n: int,
    frames: int = 180,
    interval: float = 30,
    revolutions: float = 1.0,
    show_trail: bool = True,
    figsize: tuple[float, float] = (6.5, 6.5),
) -> FuncAnimation:
    """Construye una animación Matplotlib de la órbita relativa de Bohr.

    Args:
        atom: Instancia de :class:`bohr_atom.BohrAtom`.
        n: Número cuántico principal de la órbita.
        frames: Cantidad de fotogramas del ciclo de animación.
        interval: Intervalo visual entre fotogramas, en milisegundos.
        revolutions: Número de vueltas representadas en un ciclo de animación.
        show_trail: Si es ``True``, muestra la trayectoria recorrida.
        figsize: Tamaño de la figura de Matplotlib, en pulgadas.

    Returns:
        matplotlib.animation.FuncAnimation: Animación que puede mostrarse en
        Jupyter mediante ``IPython.display.HTML(animacion.to_jshtml())``.

    Note:
        El intervalo visual no representa el período físico. La animación está
        acelerada y muestra la separación relativa electrón-núcleo.
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
            (0.0, 0.0),
            radius_pm,
            fill=False,
            linewidth=1.8,
            linestyle="--",
            alpha=0.8,
            label=f"Órbita n={n}",
        )
    )
    # El origen representa el núcleo en la coordenada relativa r = r_e - r_N.
    ax.scatter([0.0], [0.0], s=100, marker="o", zorder=5, label="Núcleo (origen)")
    trail_line, = ax.plot([], [], linewidth=2.0, alpha=0.75, label="Trayectoria")
    electron, = ax.plot(
        [],
        [],
        marker="o",
        linestyle="None",
        markersize=11,
        markeredgewidth=1.2,
        label="Electrón",
    )
    tangent = ax.annotate(
        "",
        xy=(0.0, 0.0),
        xytext=(0.0, 0.0),
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
        0.02,
        0.02,
        f"r = {radius_pm:.4f} pm\nω = {omega:.4e} rad/s\nT = {period:.4e} s",
        transform=ax.transAxes,
        va="bottom",
        ha="left",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.4", "alpha": 0.12},
    )

    def initialize_animation():
        """Inicializa los artistas gráficos antes del primer fotograma.

        Returns:
            tuple: Artistas de Matplotlib que actualizará la animación.
        """
        electron.set_data([], [])
        trail_line.set_data([], [])
        tangent.xy = (0.0, 0.0)
        tangent.set_position((0.0, 0.0))
        return electron, trail_line, tangent

    def update_animation(frame: int):
        """Actualiza posición, trayectoria y vector tangente del electrón.

        Args:
            frame: Índice del fotograma actual.

        Returns:
            tuple: Artistas de Matplotlib modificados en el fotograma.
        """
        theta = 2.0 * pi * revolutions * frame / (frames - 1)
        x_position, y_position = _phase_coordinates(radius_pm, theta)
        electron.set_data([x_position], [y_position])

        if show_trail:
            phases = np.linspace(0.0, theta, max(2, frame + 1))
            trail_line.set_data(
                radius_pm * np.cos(phases),
                radius_pm * np.sin(phases),
            )
        else:
            trail_line.set_data([], [])

        # El vector tangente muestra el sentido instantáneo de la rotación.
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
    """Crea un explorador interactivo de niveles y transiciones electrónicas.

    El panel permite modificar el número de niveles, elegir los estados inicial
    y final, y mostrar u ocultar otras transiciones descendentes. El gráfico se
    crea una sola vez y se actualiza sobre el mismo lienzo interactivo.

    Args:
        atom: Instancia de ``BohrAtom`` utilizada para calcular las energías.
        max_n: Máximo número cuántico principal disponible en los controles.

    Returns:
        ipywidgets.VBox: Panel con controles y lienzo Matplotlib interactivo.

    Raises:
        ImportError: Si no está instalado el extra ``notebooks``.
        RuntimeError: Si Matplotlib no utiliza el backend ``ipympl``.
        TypeError: Si ``max_n`` no es un entero.
        ValueError: Si ``max_n`` es menor que dos.

    Note:
        Antes de importar el módulo en Jupyter, activa el backend con
        ``%matplotlib widget``.
    """
    widgets = _import_widgets()
    _require_widget_backend()
    from .validation import validate_positive_integer

    max_n = validate_positive_integer(max_n, "max_n")
    if max_n < 2:
        raise ValueError("max_n debe ser al menos 2.")

    n_max_widget = widgets.IntSlider(
        value=min(6, max_n),
        min=2,
        max=max_n,
        step=1,
        description="Niveles visibles:",
        continuous_update=False,
        style={"description_width": "initial"},
    )
    n_initial_widget = widgets.IntSlider(
        value=min(3, max_n),
        min=1,
        max=max_n,
        step=1,
        description="Nivel inicial:",
        continuous_update=False,
        style={"description_width": "initial"},
    )
    n_final_widget = widgets.IntSlider(
        value=1,
        min=1,
        max=max_n,
        step=1,
        description="Nivel final:",
        continuous_update=False,
        style={"description_width": "initial"},
    )
    show_all_widget = widgets.Checkbox(
        value=False,
        description="Mostrar otras transiciones descendentes",
        indent=False,
    )
    status = widgets.HTML()

    # Se crea una única figura; los controles actualizan sus ejes y artistas.
    fig, ax = plt.subplots(figsize=(9.2, 5.8), constrained_layout=True)

    def update_diagram(_=None):
        """Actualiza el diagrama y los resultados tras cambiar un control.

        Args:
            _: Evento opcional enviado por un control de ``ipywidgets``.

        Returns:
            None: Actualiza el lienzo y el resumen de propiedades del fotón.
        """
        n_max = n_max_widget.value
        n_initial = n_initial_widget.value
        n_final = n_final_widget.value
        ax.clear()

        energies = {
            level: atom.energy(level, unit="eV")
            for level in range(1, n_max + 1)
        }
        for level, energy in energies.items():
            selected = level in {n_initial, n_final}
            ax.hlines(
                energy,
                0.08,
                0.58,
                linewidth=2.8 if selected else 1.5,
                alpha=1.0 if selected else 0.65,
                color="tab:blue" if selected else "0.45",
            )
            ax.text(0.04, energy, f"n={level}", ha="right", va="center")
            ax.text(
                0.61,
                energy,
                f"{energy:.5f} eV",
                ha="left",
                va="center",
                fontsize=8,
            )

        if show_all_widget.value:
            for upper in range(2, n_max + 1):
                for lower in range(1, upper):
                    if (upper, lower) == (n_initial, n_final):
                        continue
                    ax.annotate(
                        "",
                        xy=(0.84, energies[lower]),
                        xytext=(0.84, energies[upper]),
                        arrowprops={
                            "arrowstyle": "->",
                            "color": "0.65",
                            "linewidth": 0.8,
                            "alpha": 0.55,
                        },
                    )

        if n_initial == n_final:
            status.value = (
                "<b>Selecciona dos niveles diferentes.</b> "
                "Una transición requiere estados inicial y final distintos."
            )
        else:
            result = atom.transition(n_initial, n_final)
            process = "Emisión" if result["process"] == "emission" else "Absorción"
            status.value = (
                "<div style='display:flex;flex-wrap:wrap;gap:14px'>"
                f"<div><b>{process}</b><br>{n_initial} → {n_final}</div>"
                f"<div><b>Energía del fotón</b><br>"
                f"{result['photon_energy_ev']:.6f} eV</div>"
                f"<div><b>Frecuencia</b><br>{result['frequency_hz']:.4e} Hz</div>"
                f"<div><b>Longitud de onda</b><br>"
                f"{result['wavelength_nm']:.4f} nm</div>"
                "</div>"
            )
            ax.annotate(
                "",
                xy=(0.98, energies[n_final]),
                xytext=(0.98, energies[n_initial]),
                arrowprops={
                    "arrowstyle": "-|>",
                    "color": "tab:red",
                    "linewidth": 2.8,
                },
            )
            process_label = "emisión" if n_initial > n_final else "absorción"
            ax.text(
                1.02,
                0.5 * (energies[n_initial] + energies[n_final]),
                f"{n_initial} → {n_final}\n{process_label}",
                va="center",
                fontsize=9,
            )

        ax.axhline(0.0, color="0.35", linestyle=":", linewidth=1.2)
        ax.text(0.52, 0.0, "E = 0 (ionización)", va="bottom", ha="center")
        lowest_energy = min(energies.values())
        ax.set_ylim(lowest_energy * 1.15, max(0.6, abs(lowest_energy) * 0.08))
        ax.set_xlim(-0.12, 1.42)
        ax.set_xticks([])
        ax.set_ylabel("Energía (eV)")
        ax.set_title(f"Niveles energéticos — {atom.name}")
        ax.grid(axis="y", alpha=0.2)
        fig.canvas.draw_idle()

    def update_level_limits(change):
        """Ajusta los rangos de los selectores al cambiar niveles visibles.

        Args:
            change: Cambio de valor producido por el deslizador de niveles.

        Returns:
            None: Actualiza los límites de ambos selectores de transición.
        """
        new_max = change["new"]
        n_initial_widget.max = new_max
        n_final_widget.max = new_max
        if n_initial_widget.value > new_max:
            n_initial_widget.value = new_max
        if n_final_widget.value > new_max:
            n_final_widget.value = new_max

    n_max_widget.observe(update_level_limits, names="value")
    for control in (n_max_widget, n_initial_widget, n_final_widget, show_all_widget):
        control.observe(update_diagram, names="value")

    controls = widgets.VBox(
        [
            widgets.HTML(
                "<h3>Explorador de niveles energéticos</h3>"
                "<p>Modifica los niveles y observa cómo cambia la transición.</p>"
            ),
            n_max_widget,
            widgets.HBox([n_initial_widget, n_final_widget]),
            show_all_widget,
            status,
        ]
    )
    update_diagram()
    return widgets.VBox([controls, fig.canvas])


def interactive_orbit_viewer(
    atom,
    n_max: int = 6,
    frames: int = 180,
    interval: float = 35,
):
    """Crea un visor orbital animado mediante controles de ``ipywidgets``.

    El panel permite seleccionar el nivel principal, reproducir o pausar la
    rotación, controlar manualmente la fase angular, modificar la rapidez de
    reproducción y mostrar u ocultar la trayectoria y el vector tangente.
    La figura se crea una sola vez; los controles actualizan sus artistas sin
    reconstruir el gráfico en cada fotograma.

    Args:
        atom: Instancia de ``BohrAtom`` que define el sistema hidrogenoide.
        n_max: Mayor número cuántico principal disponible en el selector.
        frames: Cantidad de posiciones angulares de un ciclo visual.
        interval: Intervalo base entre posiciones, en milisegundos.

    Returns:
        ipywidgets.VBox: Panel con controles y lienzo Matplotlib interactivo.

    Raises:
        ImportError: Si no están instaladas las dependencias opcionales.
        RuntimeError: Si Matplotlib no utiliza el backend ``ipympl``.
        TypeError: Si los parámetros tienen tipos incorrectos.
        ValueError: Si los parámetros están fuera de sus dominios permitidos.

    Note:
        Antes de importar el módulo en Jupyter, activa el backend con
        ``%matplotlib widget``. El control de velocidad modifica el intervalo
        visual entre fotogramas; no cambia la velocidad angular física.
    """
    widgets = _import_widgets()
    _require_widget_backend()
    from .validation import validate_positive_integer

    n_max = validate_positive_integer(n_max, "n_max")
    if n_max < 1:
        raise ValueError("n_max debe ser al menos 1.")
    frames = _validate_frames(frames)
    interval = _validate_interval(interval)

    n_widget = widgets.IntSlider(
        value=min(2, n_max),
        min=1,
        max=n_max,
        step=1,
        description="Nivel n:",
        continuous_update=False,
        style={"description_width": "initial"},
    )
    phase_widget = widgets.IntSlider(
        value=0,
        min=0,
        max=frames - 1,
        step=1,
        description="Fase (índice):",
        continuous_update=True,
        style={"description_width": "initial"},
        layout=widgets.Layout(width="75%"),
    )
    play_widget = widgets.Play(
        value=0,
        min=0,
        max=frames - 1,
        step=1,
        interval=int(interval),
        description="Reproducir",
    )
    # El control Play conduce al deslizador, y este último actualiza la figura.
    widgets.jslink((play_widget, "value"), (phase_widget, "value"))
    speed_widget = widgets.FloatSlider(
        value=1.0,
        min=0.25,
        max=5.0,
        step=0.25,
        description="Velocidad visual:",
        readout_format=".2f",
        continuous_update=False,
        style={"description_width": "initial"},
    )
    trail_widget = widgets.Checkbox(
        value=True,
        description="Mostrar trayectoria",
        indent=False,
    )
    tangent_widget = widgets.Checkbox(
        value=True,
        description="Mostrar vector tangente",
        indent=False,
    )
    info_widget = widgets.HTML()

    # El backend ipympl convierte el lienzo de Matplotlib en un widget vivo.
    fig, ax = plt.subplots(figsize=(6.4, 6.4), constrained_layout=True)
    radius_pm = atom.radius(n_widget.value, unit="pm")
    orbit = Circle(
        (0.0, 0.0),
        radius_pm,
        fill=False,
        linestyle="--",
        linewidth=1.8,
        color="tab:blue",
        label="Órbita permitida",
    )
    ax.add_patch(orbit)
    ax.scatter(
        [0.0], [0.0], s=110, marker="o", color="tab:red",
        zorder=5, label="Núcleo",
    )
    trail_line, = ax.plot([], [], linewidth=2.0, alpha=0.75, label="Trayectoria")
    electron, = ax.plot(
        [], [], marker="o", linestyle="None", markersize=11,
        color="tab:orange", label="Electrón", zorder=6,
    )
    tangent = ax.annotate(
        "",
        xy=(0.0, 0.0),
        xytext=(0.0, 0.0),
        arrowprops={"arrowstyle": "->", "linewidth": 1.8, "color": "tab:green"},
    )
    limit = radius_pm * 1.3
    ax.set(xlim=(-limit, limit), ylim=(-limit, limit))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (pm)")
    ax.set_ylabel("y (pm)")
    ax.set_title(f"Órbita de Bohr — {atom.name}")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right")

    def update_orbit(_=None):
        """Actualiza los artistas existentes según el estado de los widgets.

        Args:
            _: Evento opcional enviado por un control de ``ipywidgets``.

        Returns:
            None: Actualiza el lienzo y el resumen de magnitudes físicas.
        """
        n = n_widget.value
        phase_fraction = phase_widget.value / (frames - 1)
        theta = 2.0 * pi * phase_fraction
        radius = atom.radius(n, unit="pm")
        x_position, y_position = _phase_coordinates(radius, theta)

        # Actualizar la circunferencia y mantener la escala proporcional al radio.
        orbit.set_radius(radius)
        limit_now = radius * 1.3
        ax.set_xlim(-limit_now, limit_now)
        ax.set_ylim(-limit_now, limit_now)
        electron.set_data([x_position], [y_position])

        if trail_widget.value and phase_widget.value > 0:
            phases = np.linspace(0.0, theta, phase_widget.value + 1)
            trail_line.set_data(
                radius * np.cos(phases),
                radius * np.sin(phases),
            )
        else:
            trail_line.set_data([], [])

        tangent_length = 0.20 * radius
        tangent.xy = (
            x_position - tangent_length * np.sin(theta),
            y_position + tangent_length * np.cos(theta),
        )
        tangent.set_position((x_position, y_position))
        tangent.set_visible(tangent_widget.value)

        omega = atom.orbital_angular_frequency(n)
        period = atom.orbital_period(n)
        info_widget.value = (
            "<div style='display:flex;flex-wrap:wrap;gap:14px'>"
            f"<div><b>Fase</b><br>{np.degrees(theta):.1f}°</div>"
            f"<div><b>Radio relativo</b><br>{radius:.5f} pm</div>"
            f"<div><b>Velocidad angular física</b><br>{omega:.4e} rad/s</div>"
            f"<div><b>Período físico</b><br>{period:.4e} s</div>"
            "</div>"
            "<small>La velocidad visual se controla por separado y no representa "
            "el período físico.</small>"
        )
        ax.set_title(f"Órbita de Bohr — {atom.name}, n={n}")
        fig.canvas.draw_idle()

    def update_speed(change):
        """Ajusta el intervalo de reproducción sin alterar el modelo físico.

        Args:
            change: Diccionario de cambio generado por el deslizador de velocidad.

        Returns:
            None: Actualiza el intervalo en milisegundos del widget Play.
        """
        play_widget.interval = max(10, int(interval / change["new"]))

    for control in (n_widget, phase_widget, trail_widget, tangent_widget):
        control.observe(update_orbit, names="value")
    speed_widget.observe(update_speed, names="value")

    controls = widgets.VBox(
        [
            widgets.HTML(
                "<h3>Visor interactivo de la órbita</h3>"
                "<p>Selecciona un nivel, reproduce la rotación o ajusta la fase.</p>"
            ),
            n_widget,
            widgets.HBox([play_widget, phase_widget]),
            speed_widget,
            widgets.HBox([trail_widget, tangent_widget]),
            info_widget,
        ]
    )
    update_orbit()
    return widgets.VBox([controls, fig.canvas])
