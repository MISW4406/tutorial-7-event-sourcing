from pydispatch import dispatcher
from .handlers import HandlerReservaDominio

dispatcher.connect(HandlerReservaDominio.handle_reserva_creada, signal='ReservaCreadaDominio')
