

from aeroalpes.modulos.vuelos.dominio.eventos import ReservaCreada
from aeroalpes.seedwork.aplicacion.handlers import Handler

class HandlerReservaDominio(Handler):

    @staticmethod
    def handle_reserva_creada(evento):
        print('================ RESERVA CREADA ===========')
        

    