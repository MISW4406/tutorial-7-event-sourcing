import asyncio
import websockets
import json

from aeroalpes.consumidor import obtener_suscripcion_a_topico

consumidor = None

async def procesar_eventos(websocket):
    global consumidor
    print(f'====== Comienza a procesar =======')
    while True:
        message = consumidor.receive()
        json_dict = json.dumps(message.value())

        print(f'Mensaje: {json_dict}')
        
        await websocket.send(json_dict)
        consumidor.acknowledge(message)
        await asyncio.sleep(1)

async def main():
    async with websockets.serve(procesar_eventos, "localhost", 5678):
        await asyncio.Future()

if __name__ == "__main__":
    consumidor = obtener_suscripcion_a_topico()
    print('========= Comenzando Servidor =========')
    asyncio.run(main())