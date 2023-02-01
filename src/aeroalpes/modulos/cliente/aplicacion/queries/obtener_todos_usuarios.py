from aeroalpes.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerTodosUsuarios(Query):
    ...

class ObtenerTodosUsuariosHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...