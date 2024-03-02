from propertiesalpes.config.db import db
from propertiesalpes.seedwork.infraestructura.uow import UnidadTrabajo, Batch
from pydispatch import dispatcher

import logging
import traceback

class ExcepcionUoW(Exception):
    ...


class UnidadTrabajoSQLAlchemy(UnidadTrabajo):

    def __init__(self):
        self._batches: list[Batch] = list()

    def __enter__(self) -> UnidadTrabajo:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _limpiar_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        # TODO Lea savepoint
        return []

    @property
    def batches(self) -> list[Batch]:
        return self._batches             

    def commit(self):
        for batch in self.batches:
            lock = batch.lock
            batch.operacion(*batch.args, **batch.kwargs)
                
        db.session.commit() # Commits the transaction

        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            db.session.rollback()
        
        super().rollback()
    
    def savepoint(self):
        # TODO Con MySQL y Postgres se debe usar el with para tener la lógica del savepoint
        # Piense como podría lograr esto ¿tal vez teniendo una lista de savepoints y momentos en el tiempo?
        ...

class UnidadTrabajoPulsar(UnidadTrabajo):

    def __init__(self):
        self._batches: list[Batch] = list()

    def __enter__(self) -> UnidadTrabajo:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _limpiar_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
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
        except:
            logging.error('ERROR: Suscribiendose al tópico de eventos!')
            traceback.print_exc()
            self.rollback(index=index)
        self._limpiar_batches()

    def rollback(self, index=None):
        # TODO Implemente la función de rollback
        # Vea los métodos agregar_evento de la clase AgregacionRaiz
        # A cada evento que se agrega, se le asigna un evento de compensación
        # Piense como podría hacer la implementación
        
        super().rollback()
    
    def savepoint(self):
        # NOTE No hay punto de implementar este método debido a la naturaleza de Event Sourcing
        ...