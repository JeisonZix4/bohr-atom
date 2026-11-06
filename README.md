# Bohr-Atom

**Biblioteca Python para estudiar y visualizar el modelo atómico de Bohr aplicado a sistemas hidrogenoides.**

Bohr-Atom implementa los cálculos analíticos del modelo de Bohr para sistemas formados por un núcleo de carga eléctrica `+Ze` y un único electrón de carga `-e`. La biblioteca incorpora la corrección por masa reducida para considerar la masa finita del núcleo y ofrece una interfaz orientada a objetos mediante la clase `BohrAtom`.

Con la biblioteca es posible calcular niveles energéticos, separaciones electrón-núcleo, propiedades de las órbitas circulares, transiciones espectrales y propiedades de los fotones emitidos o absorbidos. También incluye gráficos estáticos, widgets interactivos para Jupyter y animaciones de la coordenada relativa electrón-núcleo.

> **Alcance del modelo:** Bohr-Atom implementa un modelo semiclasico. Las circunferencias y animaciones son representaciones de las órbitas postuladas por Bohr; no representan orbitales, funciones de onda ni trayectorias físicas de la mecánica cuántica moderna.

## Contenido

- [Fundamentos físicos](#fundamentos-físicos)
- [Funcionalidades](#funcionalidades)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Ejemplo rápido](#ejemplo-rápido)
- [API de la clase `BohrAtom`](#api-de-la-clase-bohratom)
- [Ejemplos de cálculo](#ejemplos-de-cálculo)
- [Visualización y animaciones](#visualización-y-animaciones)
- [Cuadernos de Jupyter](#cuadernos-de-jupyter)
- [Pruebas y calidad del código](#pruebas-y-calidad-del-código)
- [Supuestos y limitaciones físicas](#supuestos-y-limitaciones-físicas)
- [Documentación para desarrolladores](#documentación-para-desarrolladores)
- [Referencias](#referencias)
- [Licencia](#licencia)

---

## Fundamentos físicos

### 1. Sistemas hidrogenoides

Un sistema hidrogenoide está formado por un núcleo con carga `+Ze` y un único electrón con carga `-e`. Algunos ejemplos son el hidrógeno (H), el helio ionizado (He⁺), el litio doblemente ionizado (Li²⁺) y el berilio triplemente ionizado (Be³⁺).

La interacción electrostática entre el electrón y el núcleo se describe mediante el potencial de Coulomb:

$$
V(r) = -\frac{Ze^2}{4\pi\varepsilon_0 r}.
$$

En esta expresión, `Z` es el número atómico, `e` es la magnitud de la carga elemental, `r` es la separación electrón-núcleo y `ε₀` es la permitividad eléctrica del vacío.

### 2. Cuantización del momento angular

El segundo postulado de Bohr establece que el momento angular orbital solo puede tomar valores discretos:

$$
L = \mu v r = n\hbar, \qquad n=1,2,3,\ldots
$$

Donde `μ` es la masa reducida del sistema, `v` es la rapidez relativa, `r` es la separación electrón-núcleo y `n` es el número cuántico principal.

### 3. Corrección por masa reducida

Como el núcleo también se mueve, el problema de dos cuerpos puede expresarse en la coordenada relativa mediante la masa reducida:

$$
\mu = \frac{m_e M}{m_e+M}.
$$

Aquí, `mₑ` representa la masa del electrón y `M` la masa del núcleo. En Bohr-Atom, la masa reducida se calcula durante la creación de cada objeto `BohrAtom` y se utiliza en los cálculos energéticos y orbitales.

### 4. Niveles de energía

La energía del estado estacionario con número cuántico principal `n` es:

$$
E_n = -\frac{\mu Z^2 e^4}{2(4\pi\varepsilon_0)^2\hbar^2 n^2}.
$$

El signo negativo indica que el electrón está ligado al núcleo. Se toma como referencia `E = 0` cuando la separación electrón-núcleo tiende a infinito. Para un mismo sistema, la magnitud de la energía disminuye como `1/n²` y crece como `Z²`.

### 5. Radios orbitales

La separación electrón-núcleo correspondiente al nivel `n` es:

$$
r_n = \frac{4\pi\varepsilon_0\hbar^2}{\mu e^2}\,\frac{n^2}{Z}.
$$

Por tanto, para un sistema dado, el radio crece proporcionalmente a `n²` y disminuye al aumentar `Z`. El método `radius()` devuelve esta separación relativa, no la distancia del electrón al centro de masa del átomo.

### 6. Transiciones y fotones

Para una transición desde un nivel inicial `nᵢ` hasta un nivel final `n_f`, la variación de energía del átomo se define como:

$$
\Delta E_{\mathrm{átomo}} = E_{n_f}-E_{n_i}.
$$

La energía del fotón se expresa como una magnitud positiva:

$$
E_\gamma = |\Delta E_{\mathrm{átomo}}| = h\nu = \frac{hc}{\lambda}.
$$

- **Emisión:** `nᵢ > n_f`. El átomo pasa a un estado de menor energía y emite un fotón.
- **Absorción:** `nᵢ < n_f`. El átomo absorbe un fotón y pasa a un estado de mayor energía.

La frecuencia `ν` del fotón no debe confundirse con la velocidad angular orbital `ω` del electrón en el modelo de Bohr: son magnitudes físicas distintas.

### 7. Cinemática orbital

A partir de la dinámica circular y de la cuantización del momento angular, la velocidad angular relativa de la órbita se expresa como:

$$
\omega_n = \frac{\mu Z^2 e^4}{(4\pi\varepsilon_0)^2\hbar^3 n^3}.
$$

El período de revolución es:

$$
T_n = \frac{2\pi}{\omega_n}.
$$

Estas magnitudes describen la cinemática postulada por el modelo y se utilizan como información física en las animaciones. La reproducción en pantalla está acelerada: el intervalo visual entre fotogramas no equivale al período atómico real.

---

## Funcionalidades

- Cálculo de niveles de energía en julios o electronvoltios.
- Corrección por masa reducida del núcleo.
- Cálculo de radios orbitales en metros, nanómetros, picómetros y ångströms.
- Cálculo de velocidad angular y período orbital.
- Cálculo de transiciones de emisión y absorción.
- Obtención de energía, frecuencia y longitud de onda del fotón.
- Generación de listas de niveles energéticos.
- Diagramas estáticos de niveles y transiciones.
- Representación de órbitas circulares en el plano.
- Widgets de Jupyter para explorar niveles, transiciones, fase y rotación orbital.
- Animaciones de la coordenada relativa electrón-núcleo.
- Pruebas automatizadas de propiedades matemáticas y del comportamiento del paquete.

## Estructura del proyecto

```text
Bohr-Atom/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── ESTILO_CODIGO.md
├── notebooks/
│   ├── 01_introduccion_a_bohr_atom.ipynb
│   ├── 02_niveles_energia_y_radios.ipynb
│   ├── 03_transiciones_y_espectros.ipynb
│   ├── 04_visualizacion_de_niveles_y_orbitas.ipynb
│   └── 05_visualizaciones_interactivas_y_animaciones.ipynb
├── src/
│   └── bohr_atom/
│       ├── __init__.py
│       ├── atom.py
│       ├── constants.py
│       ├── energy.py
│       ├── interactive.py
│       ├── orbit.py
│       ├── transitions.py
│       ├── validation.py
│       └── visualization.py
├── tests/
├── INTEGRACION.md
├── .gitignore
├── pyproject.toml
└── README.md
```

### Responsabilidad de los módulos

| Archivo | Responsabilidad |
|---|---|
| `constants.py` | Define las constantes físicas y las constantes derivadas utilizadas por la biblioteca. |
| `validation.py` | Valida tipos, números cuánticos y parámetros físicos de entrada. |
| `energy.py` | Calcula la masa reducida y los niveles de energía en unidades SI. |
| `orbit.py` | Calcula radios, velocidad angular y período orbital; también realiza conversiones de unidades de longitud. |
| `transitions.py` | Calcula la variación energética del átomo y las propiedades del fotón. |
| `atom.py` | Implementa la clase pública `BohrAtom` y reúne las operaciones del sistema. |
| `visualization.py` | Genera diagramas estáticos de niveles energéticos y órbitas. |
| `interactive.py` | Implementa widgets de Jupyter y animaciones orbitales. |
| `tests/` | Contiene pruebas automatizadas de los módulos y de las relaciones matemáticas. |
| `notebooks/` | Contiene ejemplos reproducibles de utilización de la biblioteca. |

---

## Instalación

### Requisitos

- Python 3.11 o superior.
- `pip`.
- Git, si se instala desde el repositorio.

### Instalar desde GitHub

Reemplaza `TU_USUARIO` por el usuario u organización propietaria del repositorio:

```bash
git clone https://github.com/TU_USUARIO/Bohr-Atom.git
cd Bohr-Atom
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Instala la biblioteca y las herramientas de desarrollo:

```bash
python -m pip install -e ".[dev]"
```

Para trabajar con notebooks y widgets interactivos, instala también las dependencias opcionales:

```bash
python -m pip install -e ".[dev,notebooks]"
```

> El nombre de distribución (el que se utiliza con `pip`) está definido por `project.name` en `pyproject.toml`. El nombre de importación de Python es `bohr_atom`; por eso se escribe `from bohr_atom import BohrAtom`. En la configuración actual, el nombre de distribución es `bohr-atom-toolkit`.

### Instalar desde PyPI

Cuando la distribución esté publicada en PyPI, podrá instalarse con:

```bash
python -m pip install bohr-atom-toolkit
```

Para utilizar los widgets y los notebooks, instala además las dependencias correspondientes o instala el proyecto desde el repositorio con el extra `notebooks`.

---

## Ejemplo rápido

```python
from bohr_atom import BohrAtom, PROTON_MASS_KG

# Crea un sistema hidrogenoide de hidrógeno.
hidrogeno = BohrAtom(
    Z=1,
    nucleus_mass_kg=PROTON_MASS_KG,
    name="Hidrógeno",
)

# Calcula la energía del estado fundamental en electronvoltios.
print(hidrogeno.energy(1, unit="eV"))

# Calcula la separación electrón-núcleo del segundo nivel en picómetros.
print(hidrogeno.radius(2, unit="pm"))

# Calcula las propiedades del fotón para la transición 3 -> 2.
print(hidrogeno.transition(3, 2))
```

Para crear un ion de helio He⁺:

```python
from bohr_atom import BohrAtom, HELIUM4_NUCLEUS_MASS_KG

helio_ionizado = BohrAtom(
    Z=2,
    nucleus_mass_kg=HELIUM4_NUCLEUS_MASS_KG,
    name="Helio ionizado (He⁺)",
)

print(helio_ionizado.energy(1, unit="eV"))
```

---

## API de la clase `BohrAtom`

La clase `BohrAtom` representa un sistema hidrogenoide concreto. Al crear una instancia se validan los parámetros físicos, se asignan las cargas del núcleo y del electrón y se calcula la masa reducida. Los métodos de cálculo utilizan esos atributos para evitar que el usuario tenga que proporcionar las mismas constantes en cada operación.

### Constructor y representación

| Método | ¿Qué hace? | Parámetros | Resultado |
|---|---|---|---|
| `__init__(Z, nucleus_mass_kg, name, electron_mass_kg)` | Inicializa el sistema, valida los parámetros, asigna las cargas eléctricas y calcula la masa reducida. | `Z`: número atómico entero positivo; `nucleus_mass_kg`: masa nuclear en kg; `name`: nombre descriptivo; `electron_mass_kg`: masa electrónica en kg. | Una instancia de `BohrAtom`. |
| `__repr__()` | Devuelve una representación textual breve del objeto, útil para inspección y depuración. | No recibe argumentos adicionales del usuario. | Cadena con el nombre, el número atómico y la masa reducida. |

### Métodos de cálculo físico

| Método | ¿Qué hace? | Parámetros | Resultado y unidades |
|---|---|---|---|
| `energy(n, unit="eV")` | Calcula la energía del estado estacionario con número cuántico principal `n`, utilizando la masa reducida de la instancia. | `n`: entero positivo; `unit`: `"J"` o `"eV"`. | Energía del nivel en julios o electronvoltios. Es negativa para estados ligados. |
| `radius(n, unit="m")` | Calcula la separación relativa electrón-núcleo correspondiente al nivel `n`. | `n`: entero positivo; `unit`: `"m"`, `"nm"`, `"pm"` o `"angstrom"`. | Separación relativa en la unidad solicitada. No es la distancia del electrón al centro de masa. |
| `orbital_angular_frequency(n)` | Calcula la velocidad angular de la coordenada relativa para la órbita circular de Bohr. | `n`: entero positivo. | Velocidad angular en rad/s. No es la frecuencia del fotón de una transición. |
| `orbital_period(n)` | Calcula el tiempo necesario para completar una revolución, a partir de la velocidad angular orbital. | `n`: entero positivo. | Período orbital en segundos. |
| `energy_levels(n_max=5, energy_unit="eV")` | Calcula los niveles desde `n=1` hasta `n=n_max`, incluyendo energía y radio orbital. | `n_max`: nivel principal máximo; `energy_unit`: `"J"` o `"eV"`. | Lista de diccionarios con las claves `n`, `energy`, `energy_unit` y `radius_pm`. No requiere Pandas. |
| `transition(n_initial, n_final)` | Compara las energías inicial y final y determina si el proceso es emisión o absorción. Calcula las propiedades del fotón. | `n_initial`: nivel inicial; `n_final`: nivel final. Ambos deben ser enteros positivos y distintos. | Diccionario con los niveles, el proceso, la variación energética del átomo, la energía del fotón en J y eV, la frecuencia en Hz y la longitud de onda en m y nm. |

### Métodos de visualización estática

| Método | ¿Qué hace? | Parámetros | Resultado |
|---|---|---|---|
| `plot_energy_levels(n_max=5, transitions=None, ax=None)` | Dibuja los niveles energéticos hasta `n_max` y conecta los estados con flechas. Si `transitions` es `None`, representa todas las transiciones descendentes entre los niveles mostrados. | `n_max`: nivel máximo; `transitions`: iterable de pares `(n_inicial, n_final)`; `ax`: ejes Matplotlib opcionales. | Tupla `(fig, ax)` con la figura y los ejes de Matplotlib. |
| `plot_orbits(levels, ax=None)` | Dibuja las circunferencias de los niveles indicados y sitúa el núcleo en el origen de la coordenada relativa. | `levels`: iterable de números cuánticos principales; `ax`: ejes Matplotlib opcionales. | Tupla `(fig, ax)` con la figura y los ejes de Matplotlib. |

### Métodos de animación e interacción

| Método | ¿Qué hace? | Parámetros | Resultado |
|---|---|---|---|
| `animate_orbit(n, **kwargs)` | Construye una animación de la posición del electrón sobre la circunferencia correspondiente al nivel `n`. Puede mostrar la trayectoria recorrida y un vector tangente. | `n`: nivel; argumentos opcionales: `frames` (fotogramas, por defecto 180), `interval` (intervalo visual en ms, por defecto 30), `revolutions` (vueltas por ciclo), `show_trail` (mostrar trayectoria) y `figsize` (tamaño de figura). | Objeto `matplotlib.animation.FuncAnimation`. En Jupyter puede mostrarse con `HTML(animacion.to_jshtml())`. |
| `interactive_energy_diagram(max_n=8)` | Crea controles para seleccionar el número máximo de niveles y los estados inicial y final. Actualiza el diagrama y presenta la clasificación del proceso y las propiedades del fotón. | `max_n`: número cuántico máximo disponible en los controles; debe ser al menos 2. | Panel `ipywidgets.VBox` compatible con JupyterLab. |
| `interactive_orbit_viewer(n_max=6, **kwargs)` | Crea un visor con selector del nivel `n`, control de fase, reproducción y opción para mostrar u ocultar la trayectoria. | `n_max`: nivel máximo del selector; `frames`: cantidad de posiciones angulares (por defecto 180); `interval`: intervalo visual entre posiciones en ms (por defecto 35). | Panel `ipywidgets.VBox` compatible con JupyterLab. |

Los tres últimos métodos requieren las dependencias opcionales de Jupyter. Instálalas con:

```bash
python -m pip install -e ".[notebooks]"
```

---

## Ejemplos de cálculo

### Consultar varios niveles energéticos

```python
# Calcula los niveles n=1, 2, 3, 4 y 5.
niveles = hidrogeno.energy_levels(n_max=5, energy_unit="eV")

for nivel in niveles:
    print(
        f"n={nivel['n']}: "
        f"E={nivel['energy']:.6f} {nivel['energy_unit']}, "
        f"r={nivel['radius_pm']:.4f} pm"
    )
```

### Analizar una transición

```python
# La transición 3 -> 2 es descendente y corresponde a emisión.
resultado = hidrogeno.transition(n_initial=3, n_final=2)

print("Proceso:", resultado["process"])
print("Energía del fotón:", resultado["photon_energy_ev"], "eV")
print("Frecuencia:", resultado["frequency_hz"], "Hz")
print("Longitud de onda:", resultado["wavelength_nm"], "nm")
```

---

## Visualización y animaciones

Los gráficos estáticos se pueden crear directamente desde una instancia:

```python
# Dibuja los primeros cinco niveles y las transiciones descendentes.
hidrogeno.plot_energy_levels(n_max=5)

# Dibuja las órbitas correspondientes a n=1, 2, 3 y 4.
hidrogeno.plot_orbits(levels=[1, 2, 3, 4])
```

Para generar una animación en Jupyter:

```python
from IPython.display import HTML, display

# Genera una animación de la órbita n=2.
animacion = hidrogeno.animate_orbit(
    n=2,
    frames=180,
    interval=30,
    revolutions=1,
    show_trail=True,
)

display(HTML(animacion.to_jshtml()))
```

Para abrir el explorador interactivo de transiciones:

```python
from IPython.display import display

display(hidrogeno.interactive_energy_diagram(max_n=8))
```

Para abrir el visor de órbitas:

```python
display(
    hidrogeno.interactive_orbit_viewer(
        n_max=6,
        frames=180,
        interval=35,
    )
)
```

Las animaciones representan la coordenada relativa electrón-núcleo. El núcleo se coloca en el origen de esa coordenada; no se dibuja por separado su movimiento alrededor del centro de masa. La velocidad de reproducción es visual y está acelerada: el intervalo entre fotogramas no representa el período físico real.

---

## Cuadernos de Jupyter

Los cuadernos de `notebooks/` muestran cómo utilizar la API pública de la biblioteca. Los cálculos se realizan mediante `BohrAtom`; los notebooks no mantienen una implementación paralela de las ecuaciones.

| Notebook | Contenido |
|---|---|
| `01_introduccion_a_bohr_atom.ipynb` | Importación, creación de sistemas hidrogenoides y primeros cálculos. |
| `02_niveles_energia_y_radios.ipynb` | Niveles energéticos, relaciones de escala y radios orbitales. |
| `03_transiciones_y_espectros.ipynb` | Emisión, absorción, energía, frecuencia y longitud de onda. |
| `04_visualizacion_de_niveles_y_orbitas.ipynb` | Diagramas energéticos y representación de órbitas circulares. |
| `05_visualizaciones_interactivas_y_animaciones.ipynb` | Widgets, controles de fase y animaciones orbitales. |

Para abrirlos desde la raíz del repositorio:

```bash
jupyter lab
```

Asegúrate de que JupyterLab utiliza el entorno virtual donde instalaste `bohr-atom` y sus dependencias opcionales.

---

## Pruebas y calidad del código

Ejecuta las pruebas desde la raíz del repositorio:

```bash
pytest -v
```

Para obtener un informe de cobertura:

```bash
pytest --cov=bohr_atom --cov-report=term-missing
```

Para revisar la calidad del código y el estilo de los docstrings:

```bash
ruff check .
```

Para comprobar el formato:

```bash
ruff format --check .
```

La configuración de Ruff utiliza convenciones de docstrings Google Style. Las pruebas comprueban propiedades matemáticas y el comportamiento del software; conviene complementarlas con comparaciones frente a referencias analíticas y datos espectroscópicos experimentales.

---

## Supuestos y limitaciones físicas

La implementación supone:

- Un sistema con un único electrón.
- Interacción electrostática de Coulomb.
- Núcleo puntual y masa nuclear finita incorporada mediante la masa reducida.
- Aproximación no relativista.
- Órbitas circulares y cuantización del momento angular según los postulados de Bohr.

No incluye correcciones relativistas, estructura fina, estructura hiperfina, espín, interacción espín-órbita, desplazamiento de Lamb, retroceso nuclear durante la emisión ni correcciones por tamaño nuclear.

Los radios calculados representan la coordenada relativa electrón-núcleo. Los dibujos de circunferencias y las animaciones ilustran el modelo de Bohr; no representan orbitales ni trayectorias de la mecánica cuántica moderna.

---

## Documentación para desarrolladores

El repositorio contiene dos documentos auxiliares con propósitos diferentes:

- [`docs/ESTILO_CODIGO.md`](docs/ESTILO_CODIGO.md): **guía permanente de estilo**. Define cómo escribir docstrings Google Style, documentar argumentos, valores de retorno, excepciones y unidades físicas, y cómo mantener el formato del código. Debe conservarse para mantener la coherencia al añadir módulos o revisar contribuciones.
- [`INTEGRACION.md`](INTEGRACION.md): **guía operativa de integración**. Explica cómo incorporar una entrega o actualización concreta al repositorio, qué archivos revisar, cómo instalar dependencias, ejecutar pruebas y crear un Pull Request. No interviene en la instalación ni en la ejecución de la biblioteca. Puede conservarse como registro del procedimiento o eliminarse cuando la integración descrita ya no sea necesaria.

Los módulos, clases y funciones utilizan docstrings en español con formato Google Style, siguiendo las convenciones generales de PEP 257. Se utilizan las secciones `Args`, `Returns`, `Raises`, `Attributes` y `Note` cuando corresponda. Las unidades de las magnitudes físicas se indican explícitamente.

---

## Referencias

1. Bohr, N. (1913). On the constitution of atoms and molecules. *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science, 26*(151), 1–25. https://doi.org/10.1080/14786441308634955
2. Ling, S. J., Sanny, J., & Moebs, W. (2016). *University Physics, Volume 3*. OpenStax. Sección 6.4: Bohr's Model of the Hydrogen Atom. https://openstax.org/books/university-physics-volume-3/pages/6-4-bohrs-model-of-the-hydrogen-atom
3. National Institute of Standards and Technology. (2022). *CODATA Recommended Values of the Fundamental Physical Constants*. https://physics.nist.gov/cuu/pdf/JPCRD2022CODATA.pdf

---

## Licencia

La licencia de distribución debe definirse explícitamente mediante un archivo `LICENSE` y declararse en `pyproject.toml`. No se debe asumir una licencia por el solo hecho de publicar el código en GitHub o PyPI.

---

**Bohr-Atom — Física atómica, programación científica y computación.**
