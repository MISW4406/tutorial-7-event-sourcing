from aeroalpes.seedwork.aplicacion.comandos import Comando, ComandoHandler

class RegistrarUsuario(Comando):
    nombres: str
    apellidos: str
    email: str
    password: str
    es_empresarial: bool

class RegistrarUsuarioHandler(ComandoHandler):
    ...