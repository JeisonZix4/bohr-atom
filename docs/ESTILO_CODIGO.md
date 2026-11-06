# Convenciones de documentación del código

El proyecto utiliza docstrings y comentarios en español para que la implementación
sea comprensible tanto desde el editor como desde herramientas de documentación.

## Docstrings

- Cada módulo comienza con un docstring que explica su responsabilidad.
- Cada clase pública documenta qué representa y cuáles son sus supuestos físicos.
- Cada función y método documenta su propósito.
- Las funciones con parámetros relevantes describen `Parameters`, `Returns` y
  `Raises` cuando corresponda.
- Las magnitudes físicas indican sus unidades en SI o en la unidad solicitada.
- Las funciones que implementan ecuaciones incluyen una explicación de la relación
  matemática utilizada y de las convenciones de signos.

## Comentarios

Los comentarios se utilizan para explicar decisiones que no son evidentes, por
 ejemplo el uso de masa reducida, el origen de coordenadas de las animaciones o
las convenciones de signo. No se comentan mecánicamente todas las líneas: un
comentario debe añadir contexto que el código por sí solo no expresa.

## Notebooks

Cada notebook incluye texto Markdown para desarrollar la teoría y comentarios
al inicio de las celdas de código para describir su propósito. Los notebooks
consumen la API pública de `bohr_atom`; no deben duplicar la implementación
de las ecuaciones físicas.

## Verificación

Se recomienda revisar periódicamente la documentación con:

```bash
ruff check .
ruff format .
pytest -v
```
