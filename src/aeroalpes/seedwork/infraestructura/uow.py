from abc import ABC, abstractmethod
from enum import Enum

from aeroalpes.seedwork.dominio.entidades import AgregacionRaiz
from pydispatch import dispatcher

import pickle
import logging
import traceback


class Lock(Enum):
    OPTIMISTA = 1
    PESIMISTA = 2

class Batch:
    def __init__(self, operacion, lock: Lock, *args, **kwargs):
        self.operacion = operacion
        self.args = args
        self.lock = lock
        self.kwargs = kwargs

class UnidadTrabajo(ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def _obtener_eventos(self, batches=None):
        batches = self.batches if batches is None else batches
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    print(arg.eventos)
                    return arg.eventos
        return list()

    @abstractmethod
    def _limpiar_batches(self):
        raise NotImplementedError

    @abstractmethod
    def batches(self) -> list[Batch]:
        raise NotImplementedError

    @abstractmethod
    def savepoints(self) -> list:
        raise NotImplementedError                    

    def commit(self):
        self._publicar_eventos_post_commit()
        self._limpiar_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        self._limpiar_batches()
    
    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    def registrar_batch(self, operacion, *args, lock=Lock.PESIMISTA, repositorio_eventos_func=None,**kwargs):
        batch = Batch(operacion, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publicar_eventos_dominio(batch, repositorio_eventos_func)

    def _publicar_eventos_dominio(self, batch, repositorio_eventos_func):
        for evento in self._obtener_eventos(batches=[batch]):
            if repositorio_eventos_func:
                repositorio_eventos_func(evento)
            dispatcher.send(signal=f'{type(evento).__name__}Dominio', evento=evento)

    def _publicar_eventos_post_commit(self):
        try:
            for evento in self._obtener_eventos():
                dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
        except:
            logging.error('ERROR: Suscribiendose al tópico de eventos!')
            traceback.print_exc()
            

def is_flask():
    try:
        from flask import session
        return True
    except Exception as e:
        return False

def registrar_unidad_de_trabajo(serialized_obj):
    from aeroalpes.config.uow import UnidadTrabajoSQLAlchemy
    from flask import session
    

    session['uow'] = serialized_obj

def flask_uow():
    from flask import session
    from aeroalpes.config.uow import UnidadTrabajoSQLAlchemy
    if session.get('uow'):
        return session['uow']
    else:
        uow_serialized = pickle.dumps(UnidadTrabajoSQLAlchemy())
        registrar_unidad_de_trabajo(uow_serialized)
        return uow_serialized

def unidad_de_trabajo() -> UnidadTrabajo:
    if is_flask():
        return pickle.loads(flask_uow())
    else:
        raise Exception('No hay unidad de trabajo')

def guardar_unidad_trabajo(uow: UnidadTrabajo):
    if is_flask():
        registrar_unidad_de_trabajo(pickle.dumps(uow))
    else:
        raise Exception('No hay unidad de trabajo')


class UnidadTrabajoPuerto:

    @staticmethod
    def commit():
        uow = unidad_de_trabajo()
        uow.commit()
        guardar_unidad_trabajo(uow)

    @staticmethod
    def rollback(savepoint=None):
        uow = unidad_de_trabajo()
        uow.rollback(savepoint=savepoint)
        guardar_unidad_trabajo(uow)

    @staticmethod
    def savepoint():
        uow = unidad_de_trabajo()
        uow.savepoint()
        guardar_unidad_trabajo(uow)

    @staticmethod
    def dar_savepoints():
        uow = unidad_de_trabajo()
        return uow.savepoints()

    @staticmethod
    def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        uow = unidad_de_trabajo()
        uow.registrar_batch(operacion, *args, lock=lock, **kwargs)
        guardar_unidad_trabajo(uow)
