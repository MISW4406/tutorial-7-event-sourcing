import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from aeroalpes.modulos.vuelos.infraestructura.schema.v1.eventos import EventoReservaCreada
from aeroalpes.modulos.vuelos.infraestructura.schema.v1.comandos import ComandoCrearReserva
from aeroalpes.modulos.vuelos.infraestructura.fabricas import FabricaRepositorio
from aeroalpes.modulos.vuelos.infraestructura.repositorios import RepositorioReservas
from aeroalpes.modulos.vuelos.dominio.entidades import Reserva
from aeroalpes.modulos.vuelos.infraestructura.dto import Reserva as ReservaDTO

from aeroalpes.seedwork.infraestructura import utils

def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-reserva', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='aeroalpes-sub-eventos', schema=AvroSchema(EventoReservaCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')

            # TODO Piense como puede desacoplar esta funcionalidad. Tal vez despachando un evento y un handler de procesamiento? Una clase servicio?
            try:
                 with app.app_context():
                    fabrica_repositorio = FabricaRepositorio()
                    repositorio = fabrica_repositorio.crear_objeto(RepositorioReservas)

                    # TODO El evento de creación no viene con todos los datos de itinerarios, esto tal vez pueda ser una extensión
                    # Asi mismo estamos dejando la funcionalidad de persistencia en el mismo método de recepción. Piense que componente
                    # podriamos diseñar para alojar esta funcionalidad
                    from aeroalpes.config.db import db

                    fecha_creacion = datetime.datetime.fromtimestamp(datos.fecha_creacion/1000.0)
                    
                    # TODO Haga los cambios necesarios para que se consideren los itinerarios, demás entidades y asociaciones
                    repositorio.agregar(Reserva(id=str(datos.id_reserva), id_cliente=str(datos.id_cliente), estado=str(datos.estado), fecha_creacion=fecha_creacion, fecha_actualizacion=fecha_creacion))
                    
                    # TODO Y si la reserva ya existe y debemos actualizarla. Complete el método para hacer merge

                    # TODO Tal vez podríamos reutilizar la Unidad de Trabajo?
                    db.session.commit()
            except:
                traceback.print_exc()
                logging.error('ERROR: Persistiendo!')

            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
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