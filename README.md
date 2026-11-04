# Bohr-Atom

**Implementación computacional del modelo atómico de Bohr para átomos hidrogenoides mediante Python.**

[![Python](https://img.shields.io/badge/Python-%3E%3D3.11-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Model](https://img.shields.io/badge/Physical%20Model-Bohr-orange)]()
[![Status](https://img.shields.io/badge/Development-In%20Progress-yellow)]()

---

## 1. Descripción del proyecto

**Bohr-Atom** es un proyecto de software científico desarrollado en Python cuyo objetivo es implementar computacionalmente el modelo atómico de Bohr para sistemas hidrogenoides.

El proyecto permite estudiar las propiedades físicas de sistemas constituidos por un núcleo de carga positiva y un único electrón, mediante la resolución analítica de las ecuaciones del modelo de Bohr.

La implementación contempla la corrección por masa reducida del sistema electrón-núcleo, permitiendo obtener resultados más precisos que los obtenidos mediante la aproximación de núcleo inmóvil.

El software está diseñado con una arquitectura modular y orientada a objetos. Los cálculos físicos, las propiedades orbitales, las transiciones espectrales y las herramientas de visualización se encuentran organizados en módulos independientes.

El propósito es construir una herramienta que permita:

- Calcular los niveles energéticos de átomos hidrogenoides.
- Obtener los radios de las órbitas permitidas.
- Estudiar las transiciones electrónicas entre estados estacionarios.
- Calcular las propiedades de los fotones emitidos o absorbidos.
- Representar gráficamente los niveles de energía y las órbitas del modelo.
- Explorar las relaciones matemáticas que describen el comportamiento de estos sistemas.

El proyecto tiene un enfoque educativo, científico y computacional. Busca conectar los fundamentos teóricos de la física atómica con su implementación mediante herramientas de programación científica.

## 2. Fundamentos físicos

### 2.1. Sistemas hidrogenoides

Un sistema hidrogenoide está constituido por un núcleo con carga eléctrica \(+Ze\) y un único electrón con carga \(-e\).

Donde:

- \(Z\) es el número atómico.
- \(e\) es la magnitud de la carga elemental.

Algunos ejemplos de sistemas hidrogenoides son:

| Sistema | Número atómico \(Z\) |
|:---|:---:|
| Hidrógeno (H) | 1 |
| Helio ionizado (He⁺) | 2 |
| Litio doblemente ionizado (Li²⁺) | 3 |
| Berilio triplemente ionizado (Be³⁺) | 4 |

La interacción entre el electrón y el núcleo está descrita por el potencial electrostático de Coulomb:

\[
V(r)=-\frac{1}{4\pi\varepsilon_0}\frac{Ze^2}{r}
\]

Donde \(\varepsilon_0\) representa la permitividad eléctrica del vacío.

### 2.2. Postulados del modelo de Bohr

El modelo se fundamenta en tres postulados:

**1. Estados estacionarios**

El electrón puede encontrarse en determinadas órbitas estacionarias permitidas, en las cuales no emite radiación electromagnética.

**2. Cuantización del momento angular**

El momento angular orbital está cuantizado:

\[
L=m_evr=n\hbar
\]

Donde:

- \(m_e\): masa del electrón.
- \(v\): velocidad orbital.
- \(r\): radio orbital.
- \(n\): número cuántico principal.
- \(\hbar\): constante de Planck reducida.

El número cuántico principal toma valores enteros positivos:

\[
n=1,2,3,\ldots
\]

**3. Transiciones electrónicas**

Las transiciones entre estados estacionarios implican la emisión o absorción de un fotón cuya energía corresponde a la diferencia energética entre los estados involucrados.

\[
E_\gamma=|E_f-E_i|=h\nu
\]

Donde \(h\) es la constante de Planck y \(\nu\) es la frecuencia del fotón.

### 2.3. Corrección por masa reducida

Para considerar que tanto el electrón como el núcleo se mueven alrededor del centro de masa del sistema, se introduce la masa reducida:

\[
\mu=\frac{m_eM}{m_e+M}
\]

Donde \(M\) es la masa del núcleo.

Esta corrección permite describir el movimiento relativo del sistema electrón-núcleo mediante un problema equivalente de una partícula con masa \(\mu\).

### 2.4. Niveles de energía

La energía permitida para un electrón en el nivel cuántico \(n\) está dada por:

\[
\boxed{
E_n=
-\frac{\mu Z^2e^4}
{2(4\pi\varepsilon_0)^2\hbar^2n^2}
}
\]

También puede expresarse mediante la energía de Rydberg:

\[
E_n=-E_R\frac{\mu}{m_e}\frac{Z^2}{n^2}
\]

Donde:

\[
E_R\approx13.605693\text{ eV}
\]

es la energía de Rydberg correspondiente a un núcleo de masa infinita.

### 2.5. Radios orbitales

Los radios permitidos se obtienen mediante:

\[
\boxed{
r_n=
\frac{4\pi\varepsilon_0\hbar^2}
{\mu e^2}
\frac{n^2}{Z}
}
\]

Para un núcleo de masa infinita, esta expresión se reduce a:

\[
r_n=a_0\frac{n^2}{Z}
\]

Donde \(a_0\) es el radio de Bohr.

### 2.6. Transiciones espectrales

Para una transición entre un estado inicial \(n_i\) y un estado final \(n_f\):

\[
\Delta E_{\text{átomo}}=E_f-E_i
\]

La energía del fotón es:

\[
E_\gamma=|\Delta E_{\text{átomo}}|
\]

La frecuencia y la longitud de onda se calculan mediante:

\[
\nu=\frac{E_\gamma}{h}
\]

\[
\lambda=\frac{c}{\nu}
\]

El proceso se clasifica como:

- **Emisión:** \(n_i>n_f\).
- **Absorción:** \(n_i<n_f\).

Estas expresiones permiten estudiar los espectros de emisión y absorción de los sistemas hidrogenoides.

---

## 3. Funcionalidades

El proyecto contempla los siguientes componentes:

| Funcionalidad | Descripción |
|:---|:---|
| Niveles energéticos | Cálculo analítico de la energía para cualquier nivel \(n\). |
| Masa reducida | Consideración de la masa finita del núcleo. |
| Radios orbitales | Cálculo de las distancias permitidas electrón-núcleo. |
| Transiciones electrónicas | Cálculo de diferencias energéticas entre estados. |
| Propiedades fotónicas | Obtención de energía, frecuencia y longitud de onda. |
| Diagramas energéticos | Representación gráfica de los estados y sus transiciones. |
| Órbitas electrónicas | Representación simplificada de las órbitas circulares. |
| Validación | Pruebas de consistencia matemática y computacional. |

## 4. Arquitectura del proyecto

El proyecto utiliza una arquitectura modular basada en Python y programación orientada a objetos.

La implementación se encuentra organizada mediante la estructura `src`, separando los cálculos físicos de las herramientas de representación gráfica.

```text
Bohr-Atom/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   ├── theory.md
│   ├── equations.md
│   └── validation.md
│
├── notebooks/
│   ├── 01_bohr_model.ipynb
│   ├── 02_energy_levels.ipynb
│   ├── 03_spectral_transitions.ipynb
│   └── 04_visualization.ipynb
│
├── src/
│   └── bohr_atom/
│       ├── __init__.py
│       ├── constants.py
│       ├── validation.py
│       ├── energy.py
│       ├── orbit.py
│       ├── transitions.py
│       ├── atom.py
│       └── visualization.py
│
├── tests/
│   ├── test_atom.py
│   ├── test_energy.py
│   ├── test_orbit.py
│   └── test_transitions.py
│
├── .gitignore
├── pyproject.toml
├── README.md
└── LICENSE
```

### 4.1. Descripción de los módulos principales

**`constants.py`**

Contiene las constantes físicas utilizadas en los cálculos:

- Carga elemental.
- Masa del electrón.
- Masa del protón.
- Masa del núcleo de helio-4.
- Permitividad eléctrica del vacío.
- Constante de Planck.
- Constante de Planck reducida.
- Velocidad de la luz.
- Radio de Bohr.
- Energía de Rydberg.

**`validation.py`**

Contiene funciones para validar los parámetros de entrada, incluyendo los números cuánticos, números atómicos y parámetros físicos positivos.

**`energy.py`**

Implementa las funciones relacionadas con el cálculo de la masa reducida y los niveles de energía.

**`orbit.py`**

Contiene los métodos matemáticos para calcular los radios orbitales y convertirlos entre diferentes unidades.

**`transitions.py`**

Implementa los cálculos de transiciones electrónicas y las propiedades de los fotones emitidos o absorbidos.

**`atom.py`**

Contiene la clase principal `BohrAtom`, que encapsula los parámetros físicos de un sistema hidrogenoide y proporciona una interfaz para realizar los cálculos.

**`visualization.py`**

Contiene las herramientas para construir representaciones gráficas de los niveles energéticos, las transiciones y las órbitas electrónicas.

**`tests/`**

Contiene las pruebas automatizadas que permiten verificar el comportamiento matemático y computacional de los módulos.

**`notebooks/`**

Contiene los cuadernos interactivos utilizados para estudiar y experimentar con el modelo.

## 5. Clase principal: BohrAtom

La clase `BohrAtom` representa un sistema hidrogenoide y encapsula sus principales parámetros físicos.

Entre sus atributos se encuentran:

| Atributo | Descripción | Unidad |
|:---|:---|:---|
| `Z` | Número atómico | Adimensional |
| `nucleus_mass_kg` | Masa del núcleo | kg |
| `electron_mass_kg` | Masa del electrón | kg |
| `reduced_mass_kg` | Masa reducida | kg |
| `electron_charge_c` | Carga del electrón | C |
| `nuclear_charge_c` | Carga del núcleo | C |
| `epsilon_0` | Permitividad del vacío | F/m |
| `planck_constant` | Constante de Planck | J·s |
| `hbar` | Constante de Planck reducida | J·s |
| `speed_of_light` | Velocidad de la luz | m/s |

La clase ofrece los siguientes métodos:

| Método | Descripción |
|:---|:---|
| `energy(n, unit)` | Calcula la energía del nivel \(n\). |
| `radius(n, unit)` | Calcula el radio orbital correspondiente. |
| `energy_levels(n_max, energy_unit)` | Genera una lista de los niveles energéticos. |
| `transition(n_initial, n_final)` | Calcula las propiedades de una transición. |
| `plot_energy_levels(n_max, transitions)` | Representa los niveles y las transiciones. |
| `plot_orbits(levels)` | Dibuja las órbitas electrónicas. |

## 6. Instalación

### 6.1. Requisitos

Se requieren:

- Python 3.11 o superior.
- pip.
- Git.
- Entorno virtual de Python.

El proyecto utiliza las siguientes dependencias:

| Biblioteca | Función |
|:---|:---|
| Matplotlib | Representación gráfica. |
| NumPy | Herramientas numéricas. |
| Pandas | Gestión de datos tabulares en los experimentos, cuando sea necesario. |
| pytest | Pruebas automatizadas. |
| pytest-cov | Análisis de cobertura de pruebas. |
| Ruff | Análisis y formato del código. |
| JupyterLab | Desarrollo de cuadernos interactivos. |

### 6.2. Clonar el repositorio

```bash
git clone https://github.com/USER/Bohr-Atom.git

cd Bohr-Atom
```

Sustituir `USER` por el nombre de usuario correspondiente de GitHub.

### 6.3. Crear un entorno virtual

```bash
python3 -m venv .venv
```

Activar el entorno virtual:

```bash
source .venv/bin/activate
```

En Windows:

```powershell
.venv\Scripts\activate
```

### 6.4. Actualizar herramientas de instalación

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 6.5. Instalar el proyecto

Se recomienda utilizar una instalación editable:

```bash
python -m pip install -e ".[dev]"
```

Esta modalidad permite modificar el código fuente y utilizar inmediatamente los cambios sin reinstalar el paquete.

## 7. Ejemplos de utilización

### 7.1. Crear un sistema hidrogenoide

Se puede importar la clase principal e instanciar un átomo de hidrógeno:

```python
from bohr_atom import BohrAtom, PROTON_MASS_KG

hydrogen = BohrAtom(
    Z=1,
    nucleus_mass_kg=PROTON_MASS_KG,
    name="Hydrogen"
)

print(hydrogen)
```

Para construir un ion de helio He⁺:

```python
from bohr_atom import (
    BohrAtom,
    HELIUM4_NUCLEUS_MASS_KG
)

helium_ion = BohrAtom(
    Z=2,
    nucleus_mass_kg=HELIUM4_NUCLEUS_MASS_KG,
    name="Helium ion"
)
```

### 7.2. Calcular niveles de energía

La energía se puede obtener en electronvoltios o julios:

```python
E1 = hydrogen.energy(1, unit="eV")

E2 = hydrogen.energy(2, unit="eV")

E3 = hydrogen.energy(3, unit="eV")

print(f"E1 = {E1:.6f} eV")
print(f"E2 = {E2:.6f} eV")
print(f"E3 = {E3:.6f} eV")
```

También se puede generar una colección de niveles:

```python
levels = hydrogen.energy_levels(
    n_max=5,
    energy_unit="eV"
)

for level in levels:
    print(level)
```

### 7.3. Calcular radios orbitales

El radio se puede obtener en diferentes unidades:

```python
r1 = hydrogen.radius(1, unit="pm")

r2 = hydrogen.radius(2, unit="pm")

r3 = hydrogen.radius(3, unit="pm")

print(f"r1 = {r1:.4f} pm")
print(f"r2 = {r2:.4f} pm")
print(f"r3 = {r3:.4f} pm")
```

Unidades disponibles:

- `m`: metros.
- `nm`: nanómetros.
- `pm`: picómetros.
- `angstrom`: ángstroms.

### 7.4. Calcular transiciones electrónicas

Para estudiar una transición desde \(n_i=3\) hasta \(n_f=2\):

```python
result = hydrogen.transition(3, 2)

for key, value in result.items():
    print(f"{key}: {value}")
```

El resultado proporciona:

- Estado inicial.
- Estado final.
- Tipo de proceso.
- Variación energética del átomo.
- Energía del fotón en julios.
- Energía del fotón en electronvoltios.
- Frecuencia.
- Longitud de onda en metros.
- Longitud de onda en nanómetros.

La transición \(3\rightarrow2\) corresponde a una línea de la serie de Balmer.

### 7.5. Representar los niveles de energía

```python
hydrogen.plot_energy_levels(
    n_max=5
)
```

También es posible seleccionar las transiciones que se desean representar:

```python
hydrogen.plot_energy_levels(
    n_max=5,
    transitions=[
        (3, 2),
        (4, 2),
        (5, 2)
    ]
)
```

Las transiciones se representan mediante flechas que conectan los niveles energéticos.

### 7.6. Representar las órbitas electrónicas

```python
hydrogen.plot_orbits(
    levels=[1, 2, 3, 4]
)
```

Esta representación muestra las órbitas circulares correspondientes a distintos valores del número cuántico principal.

**Nota:** estas órbitas son una representación conceptual propia del modelo de Bohr. No deben interpretarse como trayectorias físicas del electrón en la mecánica cuántica moderna.

## 8. Pruebas y validación

La validación del software constituye una parte fundamental del proyecto.

Se utiliza `pytest` para comprobar las relaciones matemáticas y el comportamiento de las funciones implementadas.

Entre las propiedades que se pretende verificar se encuentran:

### 8.1. Energía negativa en estados ligados

\[
E_n<0
\]

### 8.2. Dependencia energética con el número cuántico

\[
E_n\propto\frac{1}{n^2}
\]

Por tanto:

\[
E_2=\frac{E_1}{4}
\]

\[
E_3=\frac{E_1}{9}
\]

### 8.3. Dependencia del radio orbital

\[
r_n\propto n^2
\]

### 8.4. Conservación de la energía en las transiciones

\[
E_\gamma=|\Delta E_{\text{átomo}}|
\]

### 8.5. Relaciones entre energía, frecuencia y longitud de onda

\[
E_\gamma=h\nu
\]

\[
c=\lambda\nu
\]

Para ejecutar las pruebas:

```bash
pytest -v
```

Para generar un informe de cobertura:

```bash
pytest --cov=bohr_atom --cov-report=term-missing
```

Para analizar la calidad del código:

```bash
ruff check .
```

Para verificar el formato:

```bash
ruff format --check .
```

Las pruebas automáticas permiten detectar errores de implementación y verificar propiedades matemáticas. Sin embargo, no sustituyen la comparación con resultados analíticos de referencia ni la validación frente a datos experimentales.

## 9. Desarrollo y control de versiones

El proyecto utiliza Git para gestionar su historial de desarrollo y GitHub como plataforma de alojamiento.

Se recomienda trabajar mediante ramas independientes para cada funcionalidad.

Convención de nombres:

| Prefijo | Propósito |
|:---|:---|
| `feat/` | Nuevas funcionalidades. |
| `fix/` | Corrección de errores. |
| `test/` | Incorporación de pruebas. |
| `docs/` | Modificaciones de documentación. |
| `refactor/` | Mejoras estructurales. |
| `chore/` | Configuración y mantenimiento. |

Ejemplo de flujo de desarrollo:

```bash
git switch main

git pull --ff-only origin main

git switch -c feat/new-functionality

# Desarrollo y pruebas

git add .

git commit -m "feat: implement new functionality"

git push -u origin feat/new-functionality
```

Posteriormente se crea un Pull Request hacia `main`, donde se revisan e integran los cambios.

El proyecto también contempla incorporar:

- Integración continua mediante GitHub Actions.
- Validación automática de pruebas.
- Revisión del código mediante Ruff.
- Protección de la rama principal.
- Versionamiento semántico.
- Etiquetas y publicaciones de versiones.

## 10. Aproximaciones y limitaciones físicas

El modelo de Bohr constituye una aproximación histórica importante para comprender la cuantización de la energía y los espectros de sistemas hidrogenoides.

Sin embargo, tiene limitaciones que deben considerarse al interpretar sus resultados.

La implementación actual contempla:

- Sistemas de un único electrón.
- Interacción electrostática de Coulomb.
- Núcleo puntual.
- Aproximación no relativista.
- Cuantización del momento angular.
- Corrección por masa reducida.

No contempla:

- Correcciones relativistas.
- Estructura fina.
- Estructura hiperfina.
- Espín electrónico.
- Interacción espín-órbita.
- Desplazamiento de Lamb.
- Correcciones por tamaño nuclear.
- Funciones de onda y distribuciones de probabilidad de la mecánica cuántica.

Por consiguiente, los resultados deben interpretarse dentro del dominio de validez del modelo de Bohr.

La implementación no pretende sustituir una solución de la ecuación de Schrödinger, sino proporcionar una herramienta computacional para estudiar el modelo y sus predicciones analíticas.

## 11. Posibles extensiones

Se plantean las siguientes líneas de desarrollo:

**Espectros atómicos**

- Implementación de las series de Lyman, Balmer, Paschen y otras.
- Construcción de diagramas espectrales.
- Comparación con valores experimentales.
- Estudio de transiciones y reglas de selección.

**Ampliación del modelo físico**

- Comparación con la solución de la ecuación de Schrödinger.
- Estudio de los números cuánticos del modelo cuántico moderno.
- Incorporación de correcciones relativistas.
- Estudio de la estructura fina del hidrógeno.

**Desarrollo computacional**

- Mejoras en la arquitectura y API.
- Incorporación de documentación automática.
- Ampliación de las pruebas científicas.
- Desarrollo de interfaces interactivas.
- Publicación del paquete para su instalación mediante pip.

**Reproducibilidad científica**

- Incorporación de fuentes bibliográficas.
- Registro de versiones de constantes físicas.
- Validación con resultados de referencia.
- Documentación de las aproximaciones y errores numéricos.

## 12. Referencias bibliográficas

1. Bohr, N. (1913). On the constitution of atoms and molecules. *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science, 26*(151), 1–25. https://doi.org/10.1080/14786441308634955

2. Ling, S. J., Sanny, J., & Moebs, W. (2016). *University Physics, Volume 3*. OpenStax. Sección 6.4: Bohr's Model of the Hydrogen Atom. https://openstax.org/books/university-physics-volume-3/pages/6-4-bohrs-model-of-the-hydrogen-atom

3. National Institute of Standards and Technology (NIST). (2022). *CODATA Recommended Values of the Fundamental Physical Constants*. https://physics.nist.gov/cuu/pdf/JPCRD2022CODATA.pdf

## 13. Licencia

Este proyecto está destinado al desarrollo y estudio de herramientas computacionales para física atómica.

La licencia y las condiciones de distribución se encuentran especificadas en el archivo `LICENSE`.

---

**Bohr-Atom — Física teórica, programación científica y computación.**
