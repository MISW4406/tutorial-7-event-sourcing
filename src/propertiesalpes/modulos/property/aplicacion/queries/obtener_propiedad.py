from propertiesalpes.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerPropiedad(Query):
    listing_id: uuid.UUID


class ObtenerPropiedadHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...
