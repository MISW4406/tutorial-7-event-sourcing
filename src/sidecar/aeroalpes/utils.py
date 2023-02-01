from google.protobuf.timestamp_pb2 import Timestamp
from aeroalpes.pb2py import vuelos_pb2
from aeroalpes.pb2py import vuelos_pb2_grpc

def dict_a_proto_locacion(dict_locacion):
    return vuelos_pb2.Locacion(codigo=dict_locacion.get('codigo'), nombre=dict_locacion.get('nombre'))

def dict_a_proto_itinerarios(list_itinerarios):
    itinerarios = list()
    for itin in list_itinerarios:
        odos = list()
        for odo in itin.get('odos', []):
            segmentos = list()
            for seg in odo.get('segmentos', []):
                legs = list()
                for leg in seg.get('legs', []):
                    origen = dict_a_proto_locacion(leg['origen'])
                    destino = dict_a_proto_locacion(leg['destino'])

                    fecha_llegada = Timestamp()
                    fecha_llegada.FromSeconds(int(leg['fecha_llegada'].timestamp()))

                    fecha_salida = Timestamp()
                    fecha_salida.FromSeconds(int(leg['fecha_salida'].timestamp()))

                    
                    legs.append(vuelos_pb2.Leg(fecha_llegada=fecha_llegada, fecha_salida=fecha_salida, origen=origen, destino=destino))
                
                segmentos.append(vuelos_pb2.Segmento(legs=legs))
            odos.append(vuelos_pb2.Odo(segmentos=segmentos))
        itinerarios.append(vuelos_pb2.Itinerario(odos=odos))
    return itinerarios