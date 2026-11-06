# Integración de la documentación de código en el repositorio existente

Esta entrega contiene una versión completa y documentada del paquete, sus pruebas
y cinco notebooks de ejemplo. Está pensada para integrarse en el repositorio
`Bohr-Atom` que ya existe en GitHub.

## Archivos incluidos

- `src/bohr_atom/`: módulos de la biblioteca con docstrings y comentarios.
- `tests/`: pruebas con docstrings para cada fixture y función de prueba.
- `notebooks/`: cinco cuadernos con comentarios al inicio de cada celda ejecutable.
- `docs/ESTILO_CODIGO.md`: convenciones de documentación aplicadas.
- `.github/workflows/ci.yml`: ejemplo de integración continua.
- `pyproject.toml`: dependencias y configuración del paquete.
- `README.md`: documentación de referencia en español.

## Integración recomendada

1. Crea una rama nueva en tu repositorio:

   ```bash
   git switch main
   git pull --ff-only origin main
   git switch -c docs/docstrings-en-todo-el-proyecto
   ```

2. Respalda o confirma tus cambios locales antes de reemplazar módulos.

3. Copia `src/bohr_atom/` y `tests/` desde esta entrega a la raíz del repositorio.
   Si ya agregaste pruebas propias, conserva esos archivos y combina sus cambios.

4. Copia los cinco notebooks a `notebooks/`.

5. Integra `docs/ESTILO_CODIGO.md` y el workflow de `.github/workflows/ci.yml`.

6. Compara `pyproject.toml` antes de reemplazarlo. El nombre de distribución de
   esta plantilla es `bohr-atom-toolkit`; mantén el nombre que ya registraste en
   PyPI si es diferente. El nombre del módulo Python sigue siendo `bohr_atom`.

7. Instala dependencias y verifica:

   ```bash
   python -m pip install -e ".[dev,notebooks]"
   pytest -v
   ruff check .
   ruff format --check .
   ```

8. Revisa el diff, haz commit y abre un Pull Request.

## Convención de documentación

Se utiliza **Google Style Docstrings**, siguiendo las recomendaciones generales
de PEP 257. Los encabezados de sección son `Args:`, `Returns:`, `Raises:`,
`Yields:`, `Attributes:`, `Examples:` y `Note:` según corresponda. Los nombres
de argumentos coinciden con la firma de cada función y las magnitudes físicas
incluyen sus unidades.

Ruff valida esta convención mediante `pydocstyle`. La configuración está en
`pyproject.toml`, bajo `[tool.ruff.lint.pydocstyle]`, con `convention = "google"`;
además, el conjunto de reglas `D` está habilitado.

Los comentarios se reservan para justificar decisiones físicas o computacionales
que no se deducen de forma inmediata del código. Cada celda de código de los
notebooks comienza con un comentario que resume su objetivo.

No se añade un comentario redundante a cada línea: la meta es explicar el código,
no duplicarlo en lenguaje natural.
