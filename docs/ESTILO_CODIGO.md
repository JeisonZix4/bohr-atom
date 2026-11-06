# Estándar de documentación del código

El proyecto utiliza **Google Style Docstrings**, siguiendo las convenciones
generales de PEP 257. Los docstrings y comentarios se redactan en español.

## Reglas generales

- Cada módulo, clase, función y método público tiene un docstring.
- La primera línea resume el propósito mediante una frase breve.
- Se deja una línea en blanco entre el resumen y la descripción ampliada.
- Los docstrings se delimitan con comillas triples dobles (`"""`).
- Las secciones siguen los encabezados `Args:`, `Returns:`, `Yields:`,
  `Raises:`, `Attributes:`, `Example:` y `Note:` cuando corresponda.
- Los nombres de argumentos coinciden exactamente con la firma de la función.
- Las magnitudes físicas incluyen unidades explícitas, preferentemente SI.
- Se documentan las convenciones de signos y las aproximaciones físicas.

## Ejemplo de función

```python
def energy_level(n: int, Z: int, mu: float) -> float:
    """Calcula la energía del nivel n de un átomo hidrogenoide.

    Implementa la expresión de Bohr con corrección por masa reducida.

    Args:
        n: Número cuántico principal, entero positivo.
        Z: Número atómico del núcleo.
        mu: Masa reducida electrón-núcleo en kilogramos.

    Returns:
        float: Energía del estado ligado en julios.

    Raises:
        TypeError: Si un argumento tiene un tipo no admitido.
        ValueError: Si n, Z o mu no son positivos.
    """
```

## Ejemplo de clase

```python
class BohrAtom:
    """Representa un sistema hidrogenoide mediante el modelo de Bohr.

    Args:
        Z: Número atómico del núcleo.
        nucleus_mass_kg: Masa nuclear en kilogramos.

    Note:
        Las magnitudes orbitales describen la coordenada relativa
        electrón-núcleo y utilizan la masa reducida.
    """
```

## Comentarios

Los comentarios explican decisiones físicas o computacionales que no son
evidentes a partir del código. No se comenta mecánicamente cada instrucción.

## Notebooks

Los notebooks acompañan el código con celdas Markdown y comentarios. La lógica
matemática permanece en `src/bohr_atom`; los notebooks consumen la API pública
y no duplican las ecuaciones.

## Verificación automática

Ruff aplica las reglas de docstrings de Google Style mediante pydocstyle:

```bash
ruff check src tests
ruff format --check src tests
pytest -v
```
