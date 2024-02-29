from propertiesalpes.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass, field

from .objetos_valor import Ubicacion, ValorMercado

@dataclass
class Property(Entidad):
    ubicacion: Ubicacion = field(default_factory=Ubicacion)
    valorMercado: ValorMercado = field(default_factory=ValorMercado)
    estadoActual: str = field(default_factory=str)
    tipo: str = field(default_factory=str)
