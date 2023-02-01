from aeroalpes.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerUsuario(Query):
    listing_id: uuid.UUID

class ObtenerUsuarioHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...