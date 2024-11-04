import aeroalpes.seedwork.presentacion.api as api
import json
from aeroalpes.modulos.vuelos.aplicacion.dto import ReservaDTO
from aeroalpes.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from aeroalpes.modulos.vuelos.aplicacion.mapeadores import MapeadorReservaDTOJson
from aeroalpes.modulos.vuelos.aplicacion.comandos.crear_reserva import CrearReserva
from aeroalpes.modulos.vuelos.aplicacion.queries.obtener_reserva import ObtenerReserva
from aeroalpes.seedwork.aplicacion.queries import ejecutar_query
from aeroalpes.seedwork.infraestructura.despachadores import despachador_eventos  # Importa el despachador de eventos

bp = api.crear_blueprint('vuelos', '/vuelos')

@bp.route('/reserva', methods=('POST',))
def reservar_usando_comando():
    try:
        # Asignamos el valor 'pulsar' para usar la Unidad de trabajo de Pulsar
        session['uow_metodo'] = 'pulsar'

        reserva_dict = request.json

        map_reserva = MapeadorReservaDTOJson()
        reserva_dto = map_reserva.externo_a_dto(reserva_dict)

        comando = CrearReserva(
            reserva_dto.fecha_creacion,
            reserva_dto.fecha_actualizacion,
            reserva_dto.id,
            reserva_dto.itinerarios
        )
        
        # Enviar el comando al broker de eventos de forma asíncrona usando el despachador
        despachador_eventos.publicar_comando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/reserva', methods=('GET',))
@bp.route('/reserva/<id>', methods=('GET',))
def dar_reserva_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerReserva(id))
        map_reserva = MapeadorReservaDTOJson()
        
        return map_reserva.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]
