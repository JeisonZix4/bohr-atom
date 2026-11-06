"""Funciones auxiliares para validar entradas de la biblioteca.

Estas funciones centralizan las comprobaciones para que los módulos físicos
se concentren en las ecuaciones y utilicen criterios de entrada consistentes.
"""

from math import isfinite
from numbers import Integral, Real


def validate_positive_integer(value: int, name: str = "value") -> int:
    """Valida y devuelve un entero positivo.

    Parameters
    ----------
    value:
        Valor que debe ser un entero mayor o igual que uno. Los booleanos
        se rechazan aunque Python los considere una subclase de ``int``.
    name:
        Nombre del parámetro, utilizado en el mensaje de error.

    Returns
    -------
    int
        El valor validado como entero nativo de Python.

    Raises
    ------
    TypeError
        Si el valor no es entero o es booleano.
    ValueError
        Si el entero es menor que uno.
    """
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise TypeError(f"{name} debe ser un número entero.")
    if value < 1:
        raise ValueError(f"{name} debe ser mayor o igual que 1.")
    return int(value)


def validate_positive_real(value: float, name: str = "value") -> float:
    """Valida y devuelve un número real finito estrictamente positivo.

    Parameters
    ----------
    value:
        Valor real que se desea validar.
    name:
        Nombre del parámetro, utilizado en el mensaje de error.

    Returns
    -------
    float
        El valor convertido a ``float``.

    Raises
    ------
    TypeError
        Si el valor no es real o es booleano.
    ValueError
        Si el valor no es finito o no es estrictamente positivo.
    """
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} debe ser un número real.")

    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} debe ser finito y positivo.")
    return result
