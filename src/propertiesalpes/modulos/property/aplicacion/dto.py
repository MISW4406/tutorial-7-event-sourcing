from dataclasses import dataclass, field
from propertiesalpes.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class PropiedadDTO(DTO):    
    id: str = field(default_factory=str)
    ubicacion: str
    valorMercado: float
    estadoActual: str
    tipo: str
