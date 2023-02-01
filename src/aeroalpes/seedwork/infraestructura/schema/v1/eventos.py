from .mensajes import Mensaje

class EventoIntegracion(Mensaje):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)