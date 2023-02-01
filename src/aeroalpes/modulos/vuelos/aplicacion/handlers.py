from aeroalpes.modulos.vuelos.dominio.eventos import ReservaCreada, ReservaCancelada, ReservaAprobada, ReservaPagada
from aeroalpes.seedwork.aplicacion.handlers import Handler
from aeroalpes.modulos.vuelos.infraestructura.despachadores import Despachador

class HandlerReservaIntegracion(Handler):

    @staticmethod
    def handle_reserva_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')

    @staticmethod
    def handle_reserva_cancelada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')

    @staticmethod
    def handle_reserva_aprobada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')

    @staticmethod
    def handle_reserva_pagada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')


    