import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from aeroalpes.modulos.vuelos.infraestructura.schema.v1.eventos import EventoReservaCreada
from aeroalpes.modulos.vuelos.infraestructura.schema.v1.comandos import ComandoCrearReserva
from aeroalpes.modulos.vuelos.infraestructura.fabricas import FabricaRepositorio
from aeroalpes.modulos.vuelos.infraestructura.repositorios import RepositorioReservas
from aeroalpes.modulos.vuelos.dominio.entidades import Reserva

from aeroalpes.seedwork.infraestructura import utils

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-reserva', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='aeroalpes-sub-eventos', schema=AvroSchema(EventoReservaCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')

            # TODO Piense como puede desacoplar esta funcionalidad. Tal vez despachando un evento y un handler de procesamiento?
            fabrica_repositorio = FabricaRepositorio()
            repositorio = fabrica_repositorio.crear_objeto(RepositorioReservas)

            # TODO El evento de creación no viene con todos los datos de itinerarios, esto tal vez pueda ser una extensión
            # Asi mismo estamos dejando la funcionalidad de persistencia en el mismo método de recepción. Piense que componente
            # podriamos diseñar para alojar esta funcionalidad
            repositorio.agregar(Reserva(_id=str(id_reserva), id_cliente=str(id_cliente), estado=str(estado)))

            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-reserva', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearReserva))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()