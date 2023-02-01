from abc import ABC, abstractmethod

class Vista:

    @abstractmethod
    def obtener_por(**kwargs):
        ...