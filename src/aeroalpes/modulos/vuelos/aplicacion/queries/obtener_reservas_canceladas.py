from aeroalpes.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerReservasCanceladas(Query):
    ...

class ObtenerReservasCanceladasHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...