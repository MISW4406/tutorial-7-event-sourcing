from aeroalpes.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerReservasNoPagadas(Query):
    ...

class ObtenerReservasNoPagadasHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...