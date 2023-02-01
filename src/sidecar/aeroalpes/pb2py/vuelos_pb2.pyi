from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Itinerario(_message.Message):
    __slots__ = ["id", "odos"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ODOS_FIELD_NUMBER: _ClassVar[int]
    id: str
    odos: _containers.RepeatedCompositeFieldContainer[Odo]
    def __init__(self, id: _Optional[str] = ..., odos: _Optional[_Iterable[_Union[Odo, _Mapping]]] = ...) -> None: ...

class Leg(_message.Message):
    __slots__ = ["destino", "fecha_llegada", "fecha_salida", "origen"]
    DESTINO_FIELD_NUMBER: _ClassVar[int]
    FECHA_LLEGADA_FIELD_NUMBER: _ClassVar[int]
    FECHA_SALIDA_FIELD_NUMBER: _ClassVar[int]
    ORIGEN_FIELD_NUMBER: _ClassVar[int]
    destino: Locacion
    fecha_llegada: _timestamp_pb2.Timestamp
    fecha_salida: _timestamp_pb2.Timestamp
    origen: Locacion
    def __init__(self, fecha_salida: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., fecha_llegada: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., destino: _Optional[_Union[Locacion, _Mapping]] = ..., origen: _Optional[_Union[Locacion, _Mapping]] = ...) -> None: ...

class Locacion(_message.Message):
    __slots__ = ["codigo", "nombre"]
    CODIGO_FIELD_NUMBER: _ClassVar[int]
    NOMBRE_FIELD_NUMBER: _ClassVar[int]
    codigo: str
    nombre: str
    def __init__(self, codigo: _Optional[str] = ..., nombre: _Optional[str] = ...) -> None: ...

class Odo(_message.Message):
    __slots__ = ["segmentos"]
    SEGMENTOS_FIELD_NUMBER: _ClassVar[int]
    segmentos: _containers.RepeatedCompositeFieldContainer[Segmento]
    def __init__(self, segmentos: _Optional[_Iterable[_Union[Segmento, _Mapping]]] = ...) -> None: ...

class QueryReserva(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class Reserva(_message.Message):
    __slots__ = ["fecha_actualizacion", "fecha_creacion", "id", "itinerarios"]
    FECHA_ACTUALIZACION_FIELD_NUMBER: _ClassVar[int]
    FECHA_CREACION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ITINERARIOS_FIELD_NUMBER: _ClassVar[int]
    fecha_actualizacion: _timestamp_pb2.Timestamp
    fecha_creacion: _timestamp_pb2.Timestamp
    id: str
    itinerarios: _containers.RepeatedCompositeFieldContainer[Itinerario]
    def __init__(self, id: _Optional[str] = ..., fecha_creacion: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., fecha_actualizacion: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., itinerarios: _Optional[_Iterable[_Union[Itinerario, _Mapping]]] = ...) -> None: ...

class RespuestaReserva(_message.Message):
    __slots__ = ["mensaje", "reserva"]
    MENSAJE_FIELD_NUMBER: _ClassVar[int]
    RESERVA_FIELD_NUMBER: _ClassVar[int]
    mensaje: str
    reserva: Reserva
    def __init__(self, mensaje: _Optional[str] = ..., reserva: _Optional[_Union[Reserva, _Mapping]] = ...) -> None: ...

class Segmento(_message.Message):
    __slots__ = ["legs"]
    LEGS_FIELD_NUMBER: _ClassVar[int]
    legs: _containers.RepeatedCompositeFieldContainer[Leg]
    def __init__(self, legs: _Optional[_Iterable[_Union[Leg, _Mapping]]] = ...) -> None: ...
