from propertiesalpes.seedwork.aplicacion.comandos import Comando
from propertiesalpes.modulos.property.aplicacion.dto import PropiedadDTO
from .base import crea


@dataclass
class RegistrarPropiedad(Comando):
    ubicacion: str
    valorMercado: float
    estadoActual: str
    tipo: str

class RegistrarUsuarioHandler(ComandoHandler):
    .