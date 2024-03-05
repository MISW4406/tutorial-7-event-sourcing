from propertiesalpes.seedwork.aplicacion.comandos import Comando, ComandoHandler


class RegistrarPropiedad(Comando):
    ubicacion: str
    valorMercado: float
    estadoActual: str
    tipo: str

class RegistrarPropiedadHandler(ComandoHandler):
    ...
    