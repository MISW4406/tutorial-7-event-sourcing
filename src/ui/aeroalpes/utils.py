import requests
import json
import os

from pulsar.schema import *
from fastavro.schema import parse_schema

PULSAR_ENV: str = 'PULSAR_ADDRESS'

def broker_host():
    return os.getenv(PULSAR_ENV, default="localhost")

def consultar_schema_registry(topico: str) -> dict:
    json_registry = requests.get(f'http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema').json()
    return json.loads(json_registry.get('data',{}))

def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    definicion_schema = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=definicion_schema)



