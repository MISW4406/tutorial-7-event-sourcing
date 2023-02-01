import json
import requests
import datetime
import os

from aeroalpes.pb2py.vuelos_pb2 import Reserva, RespuestaReserva
from aeroalpes.pb2py.vuelos_pb2_grpc import VuelosServicer
from aeroalpes.utils import dict_a_proto_itinerarios

from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

class Vuelos(VuelosServicer):
    HOSTNAME_ENV: str = 'AEROALPES_ADDRESS'
    REST_API_HOST: str = f'http://{os.getenv(HOSTNAME_ENV, default="localhost")}:5000'
    REST_API_ENDPOINT: str = '/vuelos/reserva'

    def CrearReserva(self, request, context):
        dict_obj = MessageToDict(request, preserving_proto_field_name=True)

        r = requests.post(f'{self.REST_API_HOST}{self.REST_API_ENDPOINT}', json=dict_obj)
        if r.status_code == 200:
            respuesta = json.loads(r.text)

            fecha_creacion_dt = datetime.datetime.strptime(respuesta['fecha_creacion'], TIMESTAMP_FORMAT)
            fecha_creacion = Timestamp()
            fecha_creacion.FromDatetime(fecha_creacion_dt)

            fecha_actualizacion_dt = datetime.datetime.strptime(respuesta['fecha_actualizacion'], TIMESTAMP_FORMAT)
            fecha_actualizacion = Timestamp()
            fecha_actualizacion.FromDatetime(fecha_actualizacion_dt)

            # Transformamos en 
            itinerarios = respuesta.get('itinerarios', [])
            legs = itinerarios[0]['odos'][0]['segmentos'][0]['legs']

            for leg in legs:
                leg['fecha_salida'] = datetime.datetime.strptime(leg['fecha_salida'], TIMESTAMP_FORMAT)
                leg['fecha_llegada'] = datetime.datetime.now()


            reserva =  Reserva(id=respuesta.get('id'), 
                itinerarios=dict_a_proto_itinerarios(itinerarios), 
                fecha_actualizacion=fecha_actualizacion, 
                fecha_creacion=fecha_creacion)

            return RespuestaReserva(mensaje='OK', reserva=reserva)
        else:
            return RespuestaReserva(mensaje=f'Error: {r.status_code}')

    def ConsultarReserva(self, request, context):
        # TODO Complete esta funcionalidad
        raise NotImplementedError