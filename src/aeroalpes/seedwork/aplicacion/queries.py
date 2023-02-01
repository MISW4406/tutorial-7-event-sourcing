from functools import singledispatch
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Query(ABC):
    ...

@dataclass
class QueryResultado:
    resultado: None

class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query) -> QueryResultado:
        raise NotImplementedError()

@singledispatch
def ejecutar_query(query):
    raise NotImplementedError(f'No existe implementación para el query de tipo {type(query).__name__}')