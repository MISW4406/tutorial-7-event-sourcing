from concurrent import futures
import logging

import grpc
from aeroalpes.pb2py import vuelos_pb2
from aeroalpes.pb2py import vuelos_pb2_grpc


from aeroalpes.servicios.vuelos import Vuelos

def agregar_servicios(servidor):
    vuelos_pb2_grpc.add_VuelosServicer_to_server(Vuelos(), servidor)

def serve():
    port = '50051'
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agregar_servicios(servidor)

    servidor.add_insecure_port('[::]:' + port)
    servidor.start()
    print("Servidor corriendo por el puerto:" + port)
    servidor.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()