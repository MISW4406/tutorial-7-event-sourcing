"""Objetos valor del dominio de cliente

En este archivo usted encontrará los objetos valor del dominio de cliente

"""

from propertiesalpes.seedwork.dominio.objetos_valor import ObjetoValor, Ciudad
from dataclasses import dataclass


@dataclass(frozen=True)
class Ubicacion(ObjetoValor):
    ubicacion: str
    ciudad: Ciudad


@dataclass(frozen=True)
class ValorMercado(ObjetoValor):
    valor: float
    moneda: str
