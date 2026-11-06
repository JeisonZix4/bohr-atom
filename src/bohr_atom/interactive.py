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
    interval: float = 20,
    revolutions: float = 1.0,
    show_trail: bool = True,
    trail_length: int = 48,
    figsize: tuple[float, float] = (6.0, 6.0),
) -> FuncAnimation:
    """Construye una animación 2D optimizada de la órbita de Bohr.

    Las coordenadas de todos los fotogramas se calculan una sola vez. Durante
    la reproducción solo se actualizan el electrón, el vector tangente y una
    ventana limitada de la trayectoria. En lienzos compatibles se activa
    blitting para redibujar únicamente esos artistas dinámicos.

    Args:
        atom: Instancia de ``bohr_atom.BohrAtom``.
        n: Número cuántico principal de la órbita.
        frames: Número de fotogramas por ciclo visual.
        interval: Tiempo objetivo entre fotogramas, en milisegundos. Un valor
            de 20 ms corresponde a un objetivo de 50 FPS.
        revolutions: Número de vueltas representadas por ciclo.
        show_trail: Indica si se muestra la trayectoria reciente.
        trail_length: Número máximo de puntos que conserva la estela.
        figsize: Tamaño de la figura, en pulgadas.

    Returns:
        matplotlib.animation.FuncAnimation: Animación optimizada para mostrarse
        en Jupyter o guardarse como vídeo/HTML.

    Raises:
        TypeError: Si los parámetros enteros o reales tienen tipos inválidos.
        ValueError: Si algún parámetro no es positivo o no es finito.

    Note:
        El intervalo controla el tiempo de pantalla, no el período físico del
        electrón. La trayectoria representa la coordenada relativa electrón-
        núcleo. El blitting se activa solo si el backend lo soporta.
    """
    from .validation import validate_positive_integer, validate_positive_real

    n = validate_positive_integer(n, "n")
    frames = _validate_frames(frames)
    interval = _validate_interval(interval)
    revolutions = validate_positive_real(revolutions, "revolutions")
    trail_length = validate_positive_integer(trail_length, "trail_length")

    radius_pm = atom.radius(n, unit="pm")
    omega = atom.orbital_angular_frequency(n)
    period = atom.orbital_period(n)

    # Precalcular posiciones evita crear arreglos con np.linspace en cada frame.
    phases = np.linspace(0.0, 2.0 * pi * revolutions, frames, endpoint=True)
    x_positions = radius_pm * np.cos(phases)
    y_positions = radius_pm * np.sin(phases)

    fig, ax = plt.subplots(figsize=figsize, dpi=90, constrained_layout=False)
    ax.add_patch(
        Circle(
            (0.0, 0.0), radius_pm, fill=False, linewidth=1.5,
            linestyle="--", alpha=0.65, label=f"Órbita n={n}",
        )
    )
    # El núcleo se mantiene estático; solo se crean una vez los artistas móviles.
    ax.plot([0.0], [0.0], marker="o", linestyle="None", markersize=8,
            label="Núcleo", zorder=5)
    trail_line, = ax.plot([], [], linewidth=1.7, alpha=0.65, label="Trayectoria")
    electron, = ax.plot([], [], marker="o", linestyle="None", markersize=9,
                        markeredgewidth=0.8, label="Electrón", zorder=6)
    tangent = ax.annotate(
        "", xy=(0.0, 0.0), xytext=(0.0, 0.0),
        arrowprops={"arrowstyle": "->", "linewidth": 1.4},
    )

    limit = radius_pm * 1.25
    ax.set(xlim=(-limit, limit), ylim=(-limit, limit))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (pm)")
    ax.set_ylabel("y (pm)")
    ax.set_title(f"Rotación orbital — {atom.name}, n={n}")
    ax.grid(alpha=0.18)
    ax.legend(loc="upper right", fontsize=8)
    ax.text(
        0.02, 0.02,
        f"ω = {omega:.3e} rad/s\nT = {period:.3e} s",
        transform=ax.transAxes, va="bottom", ha="left", fontsize=8,
        bbox={"boxstyle": "round,pad=0.3", "alpha": 0.10},
    )

    dynamic_artists = (electron, trail_line, tangent)

    def initialize_animation():
        """Inicializa los artistas móviles antes de reproducir la animación."""
        electron.set_data([], [])
        trail_line.set_data([], [])
        tangent.xy = (0.0, 0.0)
        tangent.set_position((0.0, 0.0))
        return dynamic_artists

    def update_animation(frame: int):
        """Actualiza el estado visual usando coordenadas precalculadas.

        Args:
            frame: Índice del fotograma actual.

        Returns:
            tuple: Artistas dinámicos modificados.
        """
        frame = int(frame) % frames
        theta = phases[frame]
        x_position = x_positions[frame]
        y_position = y_positions[frame]
        electron.set_data([x_position], [y_position])

        if show_trail:
            # La estela tiene longitud acotada: el coste no crece con el tiempo.
            first = max(0, frame - trail_length + 1)
            trail_line.set_data(
                x_positions[first:frame + 1],
                y_positions[first:frame + 1],
            )
        else:
            trail_line.set_data([], [])

        tangent_length = 0.18 * radius_pm
        tangent.xy = (
            x_position + tangent_length * np.cos(theta + pi / 2.0),
            y_position + tangent_length * np.sin(theta + pi / 2.0),
        )
        tangent.set_position((x_position, y_position))
        return dynamic_artists

    # Blitting reduce los redibujados en 2D; se desactiva automáticamente si
    # el backend actual no implementa esta capacidad.
    use_blit = bool(getattr(fig.canvas, "supports_blit", False))
    animation = FuncAnimation(
        fig,
        update_animation,
        frames=frames,
        init_func=initialize_animation,
        interval=interval,
        blit=use_blit,
        repeat=True,
        cache_frame_data=False,
    )
    fig._bohr_atom_animation = animation
    return animation

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
    interval: float = 20,
    trail_length: int = 48,
):
    """Crea un visor orbital 2D optimizado con controles de Jupyter.

    Separa las actualizaciones rápidas de fase de los cambios lentos de nivel.
    Durante la reproducción no se recalculan radios, límites, títulos ni
    estadísticas; solo cambian los artistas móviles y una estela acotada.

    Args:
        atom: Instancia de ``BohrAtom`` que define el sistema hidrogenoide.
        n_max: Mayor número cuántico disponible en el selector.
        frames: Número de posiciones por revolución visual.
        interval: Intervalo base de reproducción, en milisegundos.
        trail_length: Máximo de puntos que se dibujan en la trayectoria.

    Returns:
        ipywidgets.VBox: Panel con controles y lienzo Matplotlib interactivo.

    Raises:
        ImportError: Si no está instalado el extra ``notebooks``.
        RuntimeError: Si no está activo el backend interactivo de ipympl.
        TypeError: Si los parámetros tienen tipos incorrectos.
        ValueError: Si los parámetros están fuera de sus dominios.

    Note:
        El backend recomendado es ``%matplotlib widget``. El intervalo controla
        la velocidad de reproducción visual, no el período físico del sistema.
    """
    widgets = _import_widgets()
    _require_widget_backend()
    from .validation import validate_positive_integer

    n_max = validate_positive_integer(n_max, "n_max")
    frames = _validate_frames(frames)
    interval = _validate_interval(interval)
    trail_length = validate_positive_integer(trail_length, "trail_length")

    n_widget = widgets.IntSlider(
        value=min(2, n_max), min=1, max=n_max, step=1,
        description="Nivel n:", continuous_update=False,
        style={"description_width": "initial"},
    )
    phase_widget = widgets.IntSlider(
        value=0, min=0, max=frames - 1, step=1,
        description="Fase:", continuous_update=True,
        style={"description_width": "initial"},
        layout=widgets.Layout(width="75%"),
    )
    play_widget = widgets.Play(
        value=0, min=0, max=frames - 1, step=1,
        interval=int(interval), description="Reproducir",
    )
    widgets.jslink((play_widget, "value"), (phase_widget, "value"))
    speed_widget = widgets.FloatSlider(
        value=1.0, min=0.5, max=3.0, step=0.25,
        description="Velocidad visual:", readout_format=".2f",
        continuous_update=False,
        style={"description_width": "initial"},
    )
    trail_widget = widgets.Checkbox(value=True, description="Mostrar trayectoria", indent=False)
    tangent_widget = widgets.Checkbox(value=True, description="Mostrar velocidad", indent=False)
    info_widget = widgets.HTML()

    # Crear la figura y todos sus artistas una sola vez.
    fig, ax = plt.subplots(figsize=(5.8, 5.8), dpi=90, constrained_layout=False)
    radius_cache = {n: atom.radius(n, unit="pm") for n in range(1, n_max + 1)}
    radius = radius_cache[n_widget.value]
    orbit = Circle((0.0, 0.0), radius, fill=False, linestyle="--",
                   linewidth=1.5, color="tab:blue", alpha=0.7, label="Órbita")
    ax.add_patch(orbit)
    ax.plot([0.0], [0.0], marker="o", linestyle="None", markersize=8,
            color="tab:red", label="Núcleo", zorder=5)
    trail_line, = ax.plot([], [], linewidth=1.7, alpha=0.65, label="Trayectoria")
    electron, = ax.plot([], [], marker="o", linestyle="None", markersize=9,
                        color="tab:orange", label="Electrón", zorder=6)
    tangent = ax.annotate(
        "", xy=(0.0, 0.0), xytext=(0.0, 0.0),
        arrowprops={"arrowstyle": "->", "linewidth": 1.5, "color": "tab:green"},
    )
    limit = radius * 1.25
    ax.set(xlim=(-limit, limit), ylim=(-limit, limit))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (pm)")
    ax.set_ylabel("y (pm)")
    ax.grid(alpha=0.18)
    ax.legend(loc="upper right", fontsize=8)

    phases = 2.0 * pi * np.arange(frames) / (frames - 1)

    def update_frame(_=None):
        """Actualiza exclusivamente posición, estela y vector tangente.

        Args:
            _: Evento opcional emitido por el control de fase.

        Returns:
            None: Modifica los artistas móviles y solicita un redibujado.
        """
        frame = phase_widget.value
        theta = phases[frame]
        current_radius = radius_cache[n_widget.value]
        x_position = current_radius * np.cos(theta)
        y_position = current_radius * np.sin(theta)
        electron.set_data([x_position], [y_position])

        if trail_widget.value and frame > 0:
            first = max(0, frame - trail_length + 1)
            trail_line.set_data(
                current_radius * np.cos(phases[first:frame + 1]),
                current_radius * np.sin(phases[first:frame + 1]),
            )
        else:
            trail_line.set_data([], [])

        tangent_length = 0.18 * current_radius
        tangent.xy = (
            x_position - tangent_length * np.sin(theta),
            y_position + tangent_length * np.cos(theta),
        )
        tangent.set_position((x_position, y_position))
        tangent.set_visible(tangent_widget.value)
        fig.canvas.draw_idle()

    def update_level(change):
        """Actualiza la órbita y los datos físicos solo al cambiar el nivel.

        Args:
            change: Evento emitido por el selector del número cuántico.

        Returns:
            None: Actualiza la circunferencia, los límites y la información.
        """
        n = change["new"]
        current_radius = radius_cache[n]
        orbit.set_radius(current_radius)
        limit_now = current_radius * 1.25
        ax.set_xlim(-limit_now, limit_now)
        ax.set_ylim(-limit_now, limit_now)
        ax.set_title(f"Órbita de Bohr — {atom.name}, n={n}")
        omega = atom.orbital_angular_frequency(n)
        period = atom.orbital_period(n)
        info_widget.value = (
            "<div style='display:flex;flex-wrap:wrap;gap:12px'>"
            f"<div><b>Radio</b><br>{current_radius:.4g} pm</div>"
            f"<div><b>ω física</b><br>{omega:.3e} rad/s</div>"
            f"<div><b>Período</b><br>{period:.3e} s</div></div>"
        )
        update_frame()

    def update_speed(change):
        """Modifica el intervalo del reproductor sin alterar magnitudes físicas.

        Args:
            change: Evento que contiene el multiplicador de velocidad.

        Returns:
            None: Ajusta el intervalo visual del widget Play.
        """
        play_widget.interval = max(12, int(interval / change["new"]))

    n_widget.observe(update_level, names="value")
    phase_widget.observe(update_frame, names="value")
    trail_widget.observe(update_frame, names="value")
    tangent_widget.observe(update_frame, names="value")
    speed_widget.observe(update_speed, names="value")

    controls = widgets.VBox([
        widgets.HTML("<h3>Visor orbital optimizado</h3>"),
        n_widget,
        widgets.HBox([play_widget, phase_widget]),
        speed_widget,
        widgets.HBox([trail_widget, tangent_widget]),
        info_widget,
    ])
    ax.set_title(f"Órbita de Bohr — {atom.name}, n={n_widget.value}")
    update_level({"new": n_widget.value})
    return widgets.VBox([controls, fig.canvas])

def _orbit_3d_coordinates(radius: float, phase: float, inclination: float):
    """Calcula la posición 3D de la coordenada relativa para una fase dada.

    Args:
        radius: Radio orbital en la unidad del sistema de coordenadas.
        phase: Fase angular en radianes.
        inclination: Inclinación del plano orbital en radianes.

    Returns:
        tuple: Coordenadas ``(x, y, z)`` de la posición relativa.
    """
    x = radius * np.cos(phase)
    y = radius * np.sin(phase) * np.cos(inclination)
    z = radius * np.sin(phase) * np.sin(inclination)
    return x, y, z


def animate_orbit_3d(
    atom,
    n: int,
    frames: int = 120,
    interval: float = 20,
    revolutions: float = 1.0,
    show_trail: bool = True,
    inclination_deg: float = 25.0,
    figsize: tuple[float, float] = (6.0, 5.2),
    trail_length: int = 36,
    orbit_points: int = 120,
) -> FuncAnimation:
    """Construye una animación 3D optimizada de la órbita relativa de Bohr.

    Las posiciones y los vectores tangentes se precalculan. La estela conserva
    un número limitado de puntos, la órbita estática tiene resolución moderada
    y se evitan cambios de cámara, límites y textos durante cada fotograma.
    Matplotlib 3D requiere redibujar la escena completa; por ello se minimiza
    deliberadamente el número y la complejidad de los artistas.

    Args:
        atom: Instancia de ``BohrAtom`` que define el sistema.
        n: Número cuántico principal positivo.
        frames: Número de fotogramas por ciclo de animación.
        interval: Tiempo objetivo entre fotogramas, en milisegundos.
        revolutions: Número de vueltas por ciclo visual.
        show_trail: Indica si se muestra una estela corta del electrón.
        inclination_deg: Inclinación del plano orbital, en grados.
        figsize: Tamaño de la figura, en pulgadas.
        trail_length: Número máximo de puntos que conserva la estela.
        orbit_points: Resolución de la circunferencia estática.

    Returns:
        matplotlib.animation.FuncAnimation: Animación 3D optimizada.

    Raises:
        TypeError: Si los parámetros enteros o reales tienen tipos inválidos.
        ValueError: Si los parámetros no son finitos o positivos.

    Note:
        El backend 3D de Matplotlib no ofrece blitting eficiente para esta
        escena: cada fotograma redibuja los ejes 3D. Para maximizar el
        rendimiento se usan artistas persistentes, datos precalculados, una
        estela acotada y una figura de resolución moderada. ``interval`` es
        tiempo visual y no el período físico del sistema.
    """
    from .validation import validate_positive_integer, validate_positive_real

    n = validate_positive_integer(n, "n")
    frames = _validate_frames(frames)
    interval = _validate_interval(interval)
    trail_length = validate_positive_integer(trail_length, "trail_length")
    orbit_points = validate_positive_integer(orbit_points, "orbit_points")
    revolutions = validate_positive_real(revolutions, "revolutions")
    inclination_deg = float(inclination_deg)
    if not isfinite(inclination_deg) or not 0.0 <= inclination_deg <= 180.0:
        raise ValueError("inclination_deg debe ser finito y estar entre 0 y 180.")

    radius_pm = atom.radius(n, unit="pm")
    omega = atom.orbital_angular_frequency(n)
    relative_speed = atom.relative_orbital_speed(n)
    inclination = np.deg2rad(inclination_deg)

    # Precalcular la órbita y todas las posiciones evita trabajo repetido.
    orbit_angles = np.linspace(0.0, 2.0 * pi, orbit_points, endpoint=True)
    orbit_x = radius_pm * np.cos(orbit_angles)
    orbit_y = radius_pm * np.sin(orbit_angles) * np.cos(inclination)
    orbit_z = radius_pm * np.sin(orbit_angles) * np.sin(inclination)

    phases = np.linspace(0.0, 2.0 * pi * revolutions, frames, endpoint=True)
    x_positions = radius_pm * np.cos(phases)
    y_positions = radius_pm * np.sin(phases) * np.cos(inclination)
    z_positions = radius_pm * np.sin(phases) * np.sin(inclination)
    tangent_x = -np.sin(phases)
    tangent_y = np.cos(phases) * np.cos(inclination)
    tangent_z = np.cos(phases) * np.sin(inclination)
    tangent_scale = 0.20 * radius_pm
    tip_x = x_positions + tangent_scale * tangent_x
    tip_y = y_positions + tangent_scale * tangent_y
    tip_z = z_positions + tangent_scale * tangent_z

    # Una figura más pequeña y pocos ticks reducen el coste de cada render 3D.
    fig = plt.figure(figsize=figsize, dpi=75, constrained_layout=False)
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(orbit_x, orbit_y, orbit_z, linestyle="--", alpha=0.55,
            linewidth=1.1, label="Órbita permitida")
    ax.plot([0.0], [0.0], [0.0], marker="o", linestyle="None",
            markersize=7, label="Núcleo")
    trail, = ax.plot([], [], [], linewidth=1.5, alpha=0.65, label="Estela")
    electron, = ax.plot([], [], [], marker="o", linestyle="None",
                        markersize=8, label="Electrón")
    velocity_line, = ax.plot([], [], [], linewidth=1.4,
                             label="Dirección tangencial")

    limit = 1.22 * radius_pm
    ax.set(xlim=(-limit, limit), ylim=(-limit, limit), zlim=(-limit, limit))
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlabel("x (pm)", labelpad=2)
    ax.set_ylabel("y (pm)", labelpad=2)
    ax.set_zlabel("z (pm)", labelpad=2)
    ax.set_title(f"Rotación orbital 3D — {atom.name}, n={n}", pad=8)
    ax.grid(False)
    ax.tick_params(labelsize=7, pad=0)
    ax.legend(loc="upper right", fontsize=7, framealpha=0.55)
    ax.text2D(
        0.02, 0.96,
        f"ω = {omega:.3e} rad/s\nv_rel = {relative_speed:.3e} m/s",
        transform=ax.transAxes, va="top", fontsize=8,
    )

    dynamic_artists = (trail, electron, velocity_line)

    def initialize_animation():
        """Inicializa los artistas que cambian durante la animación."""
        trail.set_data_3d([], [], [])
        electron.set_data_3d([], [], [])
        velocity_line.set_data_3d([], [], [])
        return dynamic_artists

    def update_animation(frame: int):
        """Actualiza los artistas 3D usando las posiciones precalculadas.

        Args:
            frame: Índice del fotograma actual.

        Returns:
            tuple: Artistas dinámicos actualizados.
        """
        frame = int(frame) % frames
        x = x_positions[frame]
        y = y_positions[frame]
        z = z_positions[frame]
        electron.set_data_3d([x], [y], [z])

        if show_trail and frame > 0:
            first = max(0, frame - trail_length + 1)
            trail.set_data_3d(
                x_positions[first:frame + 1],
                y_positions[first:frame + 1],
                z_positions[first:frame + 1],
            )
        else:
            trail.set_data_3d([], [], [])

        velocity_line.set_data_3d(
            [x, tip_x[frame]],
            [y, tip_y[frame]],
            [z, tip_z[frame]],
        )
        return dynamic_artists

    animation = FuncAnimation(
        fig,
        update_animation,
        frames=frames,
        init_func=initialize_animation,
        interval=interval,
        blit=False,
        repeat=True,
        cache_frame_data=False,
    )
    fig._bohr_atom_animation = animation
    return animation

def interactive_orbit_3d_viewer(
    atom,
    n_max: int = 6,
    frames: int = 120,
    interval: float = 20,
    trail_length: int = 32,
    orbit_points: int = 100,
):
    """Crea un visor 3D optimizado con controles de nivel, fase y cámara.

    La actualización de fase modifica únicamente el electrón, la estela y el
    vector tangencial. El radio, la órbita de referencia, los límites, la cámara
    y el panel de magnitudes solo se actualizan cuando cambia su control
    correspondiente. Esto evita recalcular y reconstruir la escena completa
    en cada paso del reproductor.

    Args:
        atom: Instancia de ``BohrAtom`` que define el sistema.
        n_max: Mayor número cuántico disponible en el selector.
        frames: Número de posiciones por revolución visual.
        interval: Intervalo base del reproductor, en milisegundos.
        trail_length: Máximo de puntos que conserva la estela.
        orbit_points: Resolución de la circunferencia de referencia.

    Returns:
        ipywidgets.VBox: Panel de controles y lienzo Matplotlib 3D.

    Raises:
        ImportError: Si faltan las dependencias opcionales.
        RuntimeError: Si no está activo el backend interactivo ipympl.
        TypeError: Si los parámetros tienen tipos incorrectos.
        ValueError: Si los parámetros están fuera de sus dominios.

    Note:
        El control Play actualiza la figura mediante eventos de Jupyter. El
        renderizado 3D de Matplotlib redibuja los ejes completos y tiene un
        límite de rendimiento; la estela corta y las actualizaciones selectivas
        reducen el trabajo por fotograma. Para un renderizado 3D de alta tasa
        de cuadros conviene un motor WebGL como Plotly.
    """
    widgets = _import_widgets()
    _require_widget_backend()
    from .validation import validate_positive_integer

    n_max = validate_positive_integer(n_max, "n_max")
    frames = _validate_frames(frames)
    interval = _validate_interval(interval)
    trail_length = validate_positive_integer(trail_length, "trail_length")
    orbit_points = validate_positive_integer(orbit_points, "orbit_points")

    n_widget = widgets.IntSlider(
        value=min(2, n_max), min=1, max=n_max, step=1,
        description="Nivel n:", continuous_update=False,
        style={"description_width": "initial"},
    )
    phase_widget = widgets.IntSlider(
        value=0, min=0, max=frames - 1, step=1,
        description="Fase:", continuous_update=True,
        style={"description_width": "initial"},
        layout=widgets.Layout(width="75%"),
    )
    play_widget = widgets.Play(
        value=0, min=0, max=frames - 1, step=1,
        interval=int(interval), description="Reproducir",
    )
    widgets.jslink((play_widget, "value"), (phase_widget, "value"))
    speed_widget = widgets.FloatSlider(
        value=1.0, min=0.5, max=3.0, step=0.25,
        description="Velocidad visual:", readout_format=".2f",
        continuous_update=False,
        style={"description_width": "initial"},
    )
    inclination_widget = widgets.IntSlider(
        value=25, min=0, max=180, step=5,
        description="Inclinación:", continuous_update=False,
        style={"description_width": "initial"},
    )
    elevation_widget = widgets.IntSlider(
        value=25, min=0, max=90, step=5,
        description="Elevación cámara:", continuous_update=False,
        style={"description_width": "initial"},
    )
    azimuth_widget = widgets.IntSlider(
        value=45, min=-180, max=180, step=5,
        description="Azimut cámara:", continuous_update=False,
        style={"description_width": "initial"},
    )
    trail_widget = widgets.Checkbox(value=True, description="Mostrar estela", indent=False)
    velocity_widget = widgets.Checkbox(value=True, description="Mostrar velocidad", indent=False)
    info_widget = widgets.HTML()

    # Crear una única escena; los cambios de fase nunca recrean los ejes.
    fig = plt.figure(figsize=(6.0, 5.0), dpi=75, constrained_layout=False)
    ax = fig.add_subplot(111, projection="3d")
    orbit_angles = np.linspace(0.0, 2.0 * pi, orbit_points, endpoint=True)
    phases = 2.0 * pi * np.arange(frames) / (frames - 1)
    initial_radius_pm = atom.radius(n_widget.value, unit="pm")
    initial_inclination = np.deg2rad(inclination_widget.value)
    orbit_line, = ax.plot([], [], [], linestyle="--", linewidth=1.1,
                          alpha=0.6, label="Órbita permitida")
    ax.plot([0.0], [0.0], [0.0], marker="o", linestyle="None",
            markersize=7, label="Núcleo")
    trail_line, = ax.plot([], [], [], linewidth=1.5, alpha=0.65, label="Estela")
    electron, = ax.plot([], [], [], marker="o", linestyle="None",
                        markersize=8, label="Electrón")
    velocity_line, = ax.plot([], [], [], linewidth=1.4,
                             label="Dirección tangencial")

    ax.set_xlabel("x (pm)", labelpad=2)
    ax.set_ylabel("y (pm)", labelpad=2)
    ax.set_zlabel("z (pm)", labelpad=2)
    ax.grid(False)
    ax.tick_params(labelsize=7, pad=0)
    ax.legend(loc="upper right", fontsize=7, framealpha=0.55)

    state = {"radius_pm": initial_radius_pm, "inclination": initial_inclination}

    def update_frame(_=None):
        """Actualiza solo los artistas dinámicos según la fase seleccionada.

        Args:
            _: Evento opcional enviado por el control de fase o visibilidad.

        Returns:
            None: Actualiza posición, estela y vector tangencial.
        """
        frame = phase_widget.value
        theta = phases[frame]
        radius_pm = state["radius_pm"]
        inclination = state["inclination"]
        x, y, z = _orbit_3d_coordinates(radius_pm, theta, inclination)
        electron.set_data_3d([x], [y], [z])

        if trail_widget.value and frame > 0:
            first = max(0, frame - trail_length + 1)
            trail_phases = phases[first:frame + 1]
            trail_line.set_data_3d(
                radius_pm * np.cos(trail_phases),
                radius_pm * np.sin(trail_phases) * np.cos(inclination),
                radius_pm * np.sin(trail_phases) * np.sin(inclination),
            )
        else:
            trail_line.set_data_3d([], [], [])

        if velocity_widget.value:
            direction = np.array([
                -np.sin(theta),
                np.cos(theta) * np.cos(inclination),
                np.cos(theta) * np.sin(inclination),
            ])
            tip = np.array([x, y, z]) + 0.20 * radius_pm * direction
            velocity_line.set_data_3d([x, tip[0]], [y, tip[1]], [z, tip[2]])
        else:
            velocity_line.set_data_3d([], [], [])
        fig.canvas.draw_idle()

    def update_level(change):
        """Recalcula la geometría estática solo cuando cambia el nivel.

        Args:
            change: Evento del selector de número cuántico.

        Returns:
            None: Actualiza órbita, escala y magnitudes físicas.
        """
        n = change["new"]
        radius_pm = atom.radius(n, unit="pm")
        state["radius_pm"] = radius_pm
        limit = 1.22 * radius_pm
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)
        ax.set_box_aspect((1, 1, 1))
        ax.set_title(f"Órbita 3D — {atom.name}, Z={atom.Z}, n={n}", pad=8)
        update_orbit_geometry()

        omega = atom.orbital_angular_frequency(n)
        speed = atom.relative_orbital_speed(n)
        period = atom.orbital_period(n)
        info_widget.value = (
            "<div style='display:flex;flex-wrap:wrap;gap:12px'>"
            f"<div><b>Radio</b><br>{radius_pm:.4g} pm</div>"
            f"<div><b>ω</b><br>{omega:.3e} rad/s</div>"
            f"<div><b>v relativa</b><br>{speed:.3e} m/s</div>"
            f"<div><b>Período</b><br>{period:.3e} s</div></div>"
        )
        update_frame()

    def update_orbit_geometry():
        """Actualiza la circunferencia estática al cambiar nivel o inclinación."""
        radius_pm = state["radius_pm"]
        inclination = state["inclination"]
        orbit_line.set_data_3d(
            radius_pm * np.cos(orbit_angles),
            radius_pm * np.sin(orbit_angles) * np.cos(inclination),
            radius_pm * np.sin(orbit_angles) * np.sin(inclination),
        )

    def update_inclination(change):
        """Actualiza la orientación del plano orbital y su circunferencia."""
        state["inclination"] = np.deg2rad(change["new"])
        update_orbit_geometry()
        update_frame()

    def update_camera(_=None):
        """Actualiza la cámara únicamente cuando cambian elevación o azimut."""
        ax.view_init(elev=elevation_widget.value, azim=azimuth_widget.value)
        fig.canvas.draw_idle()

    def update_speed(change):
        """Ajusta el intervalo de reproducción sin cambiar la velocidad física."""
        play_widget.interval = max(12, int(interval / change["new"]))

    n_widget.observe(update_level, names="value")
    phase_widget.observe(update_frame, names="value")
    inclination_widget.observe(update_inclination, names="value")
    elevation_widget.observe(update_camera, names="value")
    azimuth_widget.observe(update_camera, names="value")
    trail_widget.observe(update_frame, names="value")
    velocity_widget.observe(update_frame, names="value")
    speed_widget.observe(update_speed, names="value")

    controls = widgets.VBox([
        widgets.HTML(
            "<h3>Visor orbital 3D optimizado</h3>"
            "<p>La fase solo actualiza el electrón y su estela; la geometría "
            "y los datos se recalculan al cambiar nivel o inclinación.</p>"
        ),
        n_widget,
        widgets.HBox([play_widget, phase_widget]),
        speed_widget,
        inclination_widget,
        widgets.HBox([elevation_widget, azimuth_widget]),
        widgets.HBox([trail_widget, velocity_widget]),
        info_widget,
    ])
    update_level({"new": n_widget.value})
    return widgets.VBox([controls, fig.canvas])

