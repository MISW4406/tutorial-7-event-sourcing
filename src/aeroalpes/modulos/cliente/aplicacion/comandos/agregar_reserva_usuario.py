from aeroalpes.seedwork.aplicacion.comandos import Comando, ComandoHandler    

class AgregarReservaUsuario(Comando):
    id_usuario: uuid.UUID
    id_reserva: uuid.UUID

class AgregarReservaUsuarioHandler(ComandoHandler):
    ...