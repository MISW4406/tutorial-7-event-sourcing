from functools import singledispatch
from abc import ABC, abstractmethod

class Comando:
    ...

class ComandoHandler(ABC):
    @abstractmethod
    def handle(self, comando: Comando):
        raise NotImplementedError()

@singledispatch
def ejecutar_commando(comando):
    raise NotImplementedError(f'No existe implementación para el comando de tipo {type(comando).__name__}')