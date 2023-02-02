from aeroalpes.seedwork.infraestructura.vistas import Vista
from aeroalpes.modulos.vuelos.dominio.entidades import Reserva
from aeroalpes.config.db import db
from .dto import Reserva as ReservaDTO

class VistaReserva(Vista):
    def obtener_por(id=None, estado=None, id_cliente=None, **kwargs) -> [Reserva]:
        params = dict()

        if id:
            params['id'] = str(id)
        
        if estado:
            params['estado'] = str(estado)
        
        if id_cliente:
            params['id_cliente'] = str(id_cliente)
            
        # TODO Convierta ReservaDTO a Reserva y valide que la consulta es correcta
        return db.session.query(ReservaDTO).filter_by(**params)
