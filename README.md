# Bohr-Atom

**Biblioteca Python para estudiar computacionalmente el modelo atómico de Bohr en sistemas hidrogenoides.**

Bohr-Atom implementa los cálculos analíticos del modelo de Bohr para sistemas de un electrón y un núcleo de carga `+Ze`. Utiliza la masa reducida para describir el movimiento relativo electrón-núcleo y ofrece una interfaz orientada a objetos mediante la clase `BohrAtom`.

El proyecto integra cálculos físicos, visualización científica, ejemplos interactivos en Jupyter y pruebas automatizadas. Está orientado al aprendizaje de física atómica, programación científica y reproducibilidad computacional.

## Contenido

- [Fundamentos físicos](#fundamentos-físicos)
- [Funcionalidades](#funcionalidades)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Ejemplo rápido](#ejemplo-rápido)
- [Notebooks](#notebooks)
- [Visualizaciones interactivas](#visualizaciones-interactivas)
- [Pruebas y calidad](#pruebas-y-calidad)
- [Supuestos y limitaciones](#supuestos-y-limitaciones)
- [Documentación del código](#documentación-del-código)

## Fundamentos físicos

Un sistema hidrogenoide está formado por un único electrón y un núcleo de número atómico `Z`. El potencial electrostático de Coulomb es

\[
V(r)=-\frac{Ze^2}{4\pi\varepsilon_0r}.
\]

La cuantización del momento angular postulada por Bohr establece

\[
L=\mu vr=n\hbar,\qquad n=1,2,3,\ldots
\]

Para considerar la masa finita del núcleo, la masa del problema relativo es

\[
\mu=\frac{m_eM}{m_e+M}.
\]

Los niveles de energía y las separaciones permitidas electrón-núcleo son

\[
E_n=-\frac{\mu Z^2e^4}{2(4\pi\varepsilon_0)^2\hbar^2n^2},
\qquad
r_n=\frac{4\pi\varepsilon_0\hbar^2}{\mu e^2}\frac{n^2}{Z}.
\]

Para una transición desde `n_initial` hasta `n_final`, la variación energética del átomo se define como `E_final - E_initial`. La energía del fotón es su valor absoluto y satisface

\[
E_\gamma=h\nu=\frac{hc}{\lambda}.
\]

## Funcionalidades

- Cálculo de niveles de energía en julios o electronvoltios.
- Corrección por masa reducida del núcleo.
- Cálculo de radios orbitales en metros, nanómetros, picómetros y ångströms.
- Cálculo de transiciones de emisión y absorción.
- Energía, frecuencia y longitud de onda del fotón.
- Diagramas estáticos de niveles y órbitas.
- Widgets de Jupyter para explorar niveles, transiciones, fase angular y movimiento orbital.
- Animaciones orbitales con Matplotlib.
- Pruebas automatizadas de relaciones matemáticas y comportamiento del paquete.

## Estructura del proyecto

```text
Bohr-Atom/
├── .github/workflows/ci.yml
├── docs/
│   └── ESTILO_CODIGO.md
├── notebooks/
│   ├── 01_introduccion_a_bohr_atom.ipynb
│   ├── 02_niveles_energia_y_radios.ipynb
│   ├── 03_transiciones_y_espectros.ipynb
│   ├── 04_visualizacion_de_niveles_y_orbitas.ipynb
│   └── 05_visualizaciones_interactivas_y_animaciones.ipynb
├── src/bohr_atom/
│   ├── __init__.py
│   ├── atom.py
│   ├── constants.py
│   ├── energy.py
│   ├── interactive.py
│   ├── orbit.py
│   ├── transitions.py
│   ├── validation.py
│   └── visualization.py
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md
```

## Instalación

Se recomienda Python 3.11 o superior y un entorno virtual.

```bash
 git clone https://github.com/TU_USUARIO/Bohr-Atom.git
 cd Bohr-Atom
 python3 -m venv .venv
 source .venv/bin/activate
 python -m pip install --upgrade pip
```

Instala el núcleo y las herramientas de desarrollo:

```bash
python -m pip install -e ".[dev]"
```

Para ejecutar los notebooks y los widgets interactivos, instala también las dependencias opcionales:

```bash
python -m pip install -e ".[dev,notebooks]"
```

> El nombre de distribución de PyPI (`bohr-atom-toolkit`, en esta plantilla) es independiente del nombre de importación Python (`bohr_atom`). Si el proyecto ya tiene un nombre registrado en PyPI, conserva ese nombre en `pyproject.toml`.

## Ejemplo rápido

```python
from bohr_atom import BohrAtom, PROTON_MASS_KG

# Construye el sistema hidrogenoide de hidrógeno.
hydrogen = BohrAtom(
    Z=1,
    nucleus_mass_kg=PROTON_MASS_KG,
    name="Hidrógeno",
)

# Calcula energía y radio del estado fundamental.
print(hydrogen.energy(1, unit="eV"))
print(hydrogen.radius(1, unit="pm"))

# Obtiene propiedades de la transición de emisión n=3 -> n=2.
print(hydrogen.transition(3, 2))
```

## Notebooks

Los cuadernos de `notebooks/` muestran cómo utilizar la API pública de la biblioteca:

| Notebook | Contenido |
|---|---|
| `01_introduccion_a_bohr_atom.ipynb` | Importación, creación de sistemas y primeros cálculos. |
| `02_niveles_energia_y_radios.ipynb` | Tablas, escalamiento energético y radios orbitales. |
| `03_transiciones_y_espectros.ipynb` | Emisión, absorción, frecuencia, longitud de onda y serie de Balmer. |
| `04_visualizacion_de_niveles_y_orbitas.ipynb` | Diagramas energéticos y órbitas circulares. |
| `05_visualizaciones_interactivas_y_animaciones.ipynb` | Widgets, controles de fase y animaciones orbitales. |

Inicia JupyterLab desde la raíz del repositorio:

```bash
jupyter lab
```

## Visualizaciones interactivas

El módulo `bohr_atom.interactive` ofrece las funciones `interactive_energy_diagram`, `interactive_orbit_viewer` y `animate_orbit`. Por ejemplo:

```python
from IPython.display import HTML, display
from bohr_atom import BohrAtom, PROTON_MASS_KG
from bohr_atom.interactive import animate_orbit, interactive_energy_diagram

# Prepara el átomo para los ejemplos interactivos.
hydrogen = BohrAtom(1, PROTON_MASS_KG, name="Hidrógeno")

# Crea un panel para seleccionar niveles inicial y final.
display(interactive_energy_diagram(hydrogen, max_n=8))

# Genera una animación ilustrativa de la órbita del nivel n=2.
orbital_animation = animate_orbit(hydrogen, n=2, frames=120)
display(HTML(orbital_animation.to_jshtml()))
```

La animación acelera la reproducción visual. El período físico se muestra como dato, pero no se reproduce en tiempo real. El dibujo representa la coordenada relativa electrón-núcleo y no una trayectoria de la mecánica cuántica moderna.

## Pruebas y calidad

Ejecuta las pruebas:

```bash
pytest -v
```

Calcula la cobertura:

```bash
pytest --cov=bohr_atom --cov-report=term-missing
```

Revisa calidad y formato:

```bash
ruff check .
ruff format .  # Aplica el formato configurado al código fuente.
```

## Supuestos y limitaciones

La implementación supone un sistema de un electrón, interacción Coulombiana, núcleo puntual, aproximación no relativista y corrección por masa reducida. No incluye estructura fina, estructura hiperfina, espín, desplazamiento de Lamb, retroceso fotónico ni correcciones por tamaño nuclear.

El modelo de Bohr es semiclasico. Las circunferencias de los gráficos no son orbitales ni trayectorias físicas del electrón en la mecánica cuántica moderna.

## Documentación del código

Los módulos, clases, funciones y métodos contienen docstrings en español. Se documentan propósito, parámetros, unidades, retornos, excepciones y supuestos físicos cuando corresponde. Los comentarios se reservan para explicar decisiones físicas o computacionales no evidentes. Cada celda de código de los notebooks comienza con un comentario que indica su objetivo.

Consulta `docs/ESTILO_CODIGO.md` para conocer estas convenciones.
