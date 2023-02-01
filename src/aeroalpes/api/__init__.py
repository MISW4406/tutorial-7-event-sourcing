import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import aeroalpes.modulos.cliente.aplicacion
    import aeroalpes.modulos.vuelos.aplicacion

def importar_modelos_alchemy():
    import aeroalpes.modulos.cliente.infraestructura.dto
    import aeroalpes.modulos.hoteles.infraestructura.dto
    import aeroalpes.modulos.pagos.infraestructura.dto
    import aeroalpes.modulos.precios_dinamicos.infraestructura.dto
    import aeroalpes.modulos.vehiculos.infraestructura.dto
    import aeroalpes.modulos.vuelos.infraestructura.dto

def comenzar_consumidor():
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener 
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """

    import threading
    import aeroalpes.modulos.cliente.infraestructura.consumidores as cliente
    import aeroalpes.modulos.hoteles.infraestructura.consumidores as hoteles
    import aeroalpes.modulos.pagos.infraestructura.consumidores as pagos
    import aeroalpes.modulos.precios_dinamicos.infraestructura.consumidores as precios_dinamicos
    import aeroalpes.modulos.vehiculos.infraestructura.consumidores as vehiculos
    import aeroalpes.modulos.vuelos.infraestructura.consumidores as vuelos

    # Suscripción a eventos
    threading.Thread(target=cliente.suscribirse_a_eventos).start()
    threading.Thread(target=hoteles.suscribirse_a_eventos).start()
    threading.Thread(target=pagos.suscribirse_a_eventos).start()
    threading.Thread(target=precios_dinamicos.suscribirse_a_eventos).start()
    threading.Thread(target=vehiculos.suscribirse_a_eventos).start()
    threading.Thread(target=vuelos.suscribirse_a_eventos).start()

    # Suscripción a comandos
    threading.Thread(target=cliente.suscribirse_a_comandos).start()
    threading.Thread(target=hoteles.suscribirse_a_comandos).start()
    threading.Thread(target=pagos.suscribirse_a_comandos).start()
    threading.Thread(target=precios_dinamicos.suscribirse_a_comandos).start()
    threading.Thread(target=vehiculos.suscribirse_a_comandos).start()
    threading.Thread(target=vuelos.suscribirse_a_comandos).start()

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from aeroalpes.config.db import init_db, database_connection

    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection(configuracion, basedir=basedir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from aeroalpes.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor()

     # Importa Blueprints
    from . import cliente
    from . import hoteles
    from . import pagos
    from . import precios_dinamicos
    from . import vehiculos
    from . import vuelos

    # Registro de Blueprints
    app.register_blueprint(cliente.bp)
    app.register_blueprint(hoteles.bp)
    app.register_blueprint(pagos.bp)
    app.register_blueprint(precios_dinamicos.bp)
    app.register_blueprint(vehiculos.bp)
    app.register_blueprint(vuelos.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
