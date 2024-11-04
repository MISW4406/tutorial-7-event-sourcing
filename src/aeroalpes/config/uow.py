from aeroalpes.config.db import db
from aeroalpes.seedwork.infraestructura.uow import UnidadTrabajo, Batch
from pydispatch import dispatcher

import logging
import traceback

class ExcepcionUoW(Exception):
    ...

class UnidadTrabajoSQLAlchemy(UnidadTrabajo):

    def __init__(self):
        self._batches: list[Batch] = list()
        self._savepoints: list = []  # Lista para almacenar savepoints

    def __enter__(self) -> UnidadTrabajo:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _limpiar_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        # Retorna la lista de savepoints
        return self._savepoints

    @property
    def batches(self) -> list[Batch]:
        return self._batches             

    def commit(self):
        for batch in self.batches:
            batch.operacion(*batch.args, **batch.kwargs)
                
        db.session.commit()  # Commits the transaction
        self._savepoints.clear()  # Limpiar los savepoints después del commit
        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            # Restaurar al savepoint indicado
            db.session.execute(f'ROLLBACK TO SAVEPOINT {savepoint}')
            self._savepoints = self._savepoints[:self._savepoints.index(savepoint)]
        else:
            db.session.rollback()
            self._savepoints.clear()  # Limpiar todos los savepoints en un rollback general
        
        super().rollback()
    
    def savepoint(self):
        # Crear un nuevo savepoint con SQLAlchemy y guardarlo en la lista de savepoints
        savepoint_name = f'savepoint_{len(self._savepoints) + 1}'
        db.session.execute(f'SAVEPOINT {savepoint_name}')
        self._savepoints.append(savepoint_name)
        return savepoint_name

class UnidadTrabajoPulsar(UnidadTrabajo):

    def __init__(self):
        self._batches: list[Batch] = list()
        self._compensation_events: list = []  # Lista para almacenar eventos de compensación

    def __enter__(self) -> UnidadTrabajo:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _limpiar_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        # No se usa savepoint en Event Sourcing
        return []

    @property
    def batches(self) -> list[Batch]:
        return self._batches             

    def commit(self):
        index = 0
        try:
            for evento in self._obtener_eventos():
                dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
                index += 1
        except Exception as e:
            logging.error('ERROR: Suscribiendose al tópico de eventos!')
            traceback.print_exc()
            self.rollback(index=index)
        self._limpiar_batches()

    def rollback(self, index=None):
        # Si ocurre un error, se ejecutan eventos de compensación
        if index is not None:
            logging.info(f'Revirtiendo desde el evento en el índice {index}')
            for i in range(index - 1, -1, -1):
                evento = self._compensation_events[i]
                dispatcher.send(signal=f'{type(evento).__name__}Compensacion', evento=evento)
        super().rollback()

    def savepoint(self):
        # No se implementa debido a la naturaleza de Event Sourcing
        pass
