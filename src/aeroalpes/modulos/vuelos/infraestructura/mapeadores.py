""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from aeroalpes.seedwork.dominio.repositorios import Mapeador
from aeroalpes.seedwork.infraestructura.utils import unix_time_millis
from aeroalpes.modulos.vuelos.dominio.objetos_valor import NombreAero, Odo, Leg, Segmento, Itinerario, CodigoIATA
from aeroalpes.modulos.vuelos.dominio.entidades import Proveedor, Aeropuerto, Reserva
from aeroalpes.modulos.vuelos.dominio.eventos import ReservaAprobada, ReservaCancelada, ReservaAprobada, ReservaPagada, ReservaCreada, EventoReserva

from .dto import Reserva as ReservaDTO
from .dto import Itinerario as ItinerarioDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosReserva(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            ReservaCreada: self._entidad_a_reserva_creada,
            ReservaAprobada: self._entidad_a_reserva_aprobada,
            ReservaCancelada: self._entidad_a_reserva_cancelada,
            ReservaPagada: self._entidad_a_reserva_pagada
        }

    def obtener_tipo(self) -> type:
        return EventoReserva.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_reserva_creada(self, entidad: ReservaCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import ReservaCreadaPayload, EventoReservaCreada

            payload = ReservaCreadaPayload(
                id_reserva=str(evento.id_reserva), 
                id_cliente=str(evento.id_cliente), 
                estado=str(evento.estado), 
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoReservaCreada(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'ReservaCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'aeroalpes'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def _entidad_a_reserva_aprobada(self, entidad: ReservaAprobada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_reserva_cancelada(self, entidad: ReservaCancelada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_reserva_pagada(self, entidad: ReservaPagada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError

    def entidad_a_dto(self, entidad: EventoReserva, version=LATEST_VERSION) -> ReservaDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: ReservaDTO, version=LATEST_VERSION) -> Reserva:
        raise NotImplementedError


class MapeadorReserva(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_itinerario_dto(self, itinerarios_dto: list) -> list[Itinerario]:
        itin_dict = dict()
        
        for itin in itinerarios_dto:
            destino = Aeropuerto(codigo=itin.destino_codigo, nombre=None)
            origen = Aeropuerto(codigo=itin.origen_codigo, nombre=None)
            fecha_salida = itin.fecha_salida
            fecha_llegada = itin.fecha_llegada

            itin_dict.setdefault(str(itin.odo_orden),{}).setdefault(str(itin.segmento_orden), {}).setdefault(str(itin.leg_orden), Leg(fecha_salida, fecha_llegada, origen, destino))

        odos = list()
        for k, odos_dict in itin_dict.items():
            segmentos = list()
            for k, seg_dict in odos_dict.items():
                legs = list()
                for k, leg in seg_dict.items():
                    legs.append(leg)
                segmentos.append(Segmento(legs))
            odos.append(Odo(segmentos))

        return [Itinerario(odos)]

    def _procesar_itinerario(self, itinerario: any) -> list[ItinerarioDTO]:
        itinerarios_dto = list()

        for i, odo in enumerate(itinerario.odos):
            for j, seg in enumerate(odo.segmentos):
                for k, leg in enumerate(seg.legs):
                    itinerario_dto = ItinerarioDTO()
                    itinerario_dto.destino_codigo = leg.destino.codigo
                    itinerario_dto.origen_codigo = leg.origen.codigo
                    itinerario_dto.fecha_salida = leg.fecha_salida
                    itinerario_dto.fecha_llegada = leg.fecha_llegada
                    itinerario_dto.leg_orden = k
                    itinerario_dto.segmento_orden = j
                    itinerario_dto.odo_orden = i

                    itinerarios_dto.append(itinerario_dto)

        return itinerarios_dto

    def obtener_tipo(self) -> type:
        return Reserva.__class__

    def entidad_a_dto(self, entidad: Reserva) -> ReservaDTO:
        
        reserva_dto = ReservaDTO()
        reserva_dto.fecha_creacion = entidad.fecha_creacion
        reserva_dto.fecha_actualizacion = entidad.fecha_actualizacion
        reserva_dto.id = str(entidad.id)

        itinerarios_dto = list()
        
        for itinerario in entidad.itinerarios:
            itinerarios_dto.extend(self._procesar_itinerario(itinerario))

        reserva_dto.itinerarios = itinerarios_dto

        return reserva_dto

    def dto_a_entidad(self, dto: ReservaDTO) -> Reserva:
        reserva = Reserva(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        reserva.itinerarios = list()

        itinerarios_dto: list[ItinerarioDTO] = dto.itinerarios

        reserva.itinerarios.extend(self._procesar_itinerario_dto(itinerarios_dto))
        
        return reserva