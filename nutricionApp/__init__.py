from flask import (
    Flask,
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    session,
    jsonify,
)

import hashlib
import Config as Config, locale, re  # Importar config.py en donde se hacen las consultas de la base de datos

class MyException(Exception):
    def __init__(self, Tipo, mensaje):
        self.Tipo = Tipo
        self.mensaje = mensaje

def create_app():
    app = Flask(__name__)

    # Configuración
    app.config["SECRET_KEY"] = Config.HEX_SEC_KEY  # Agregar la configuración del SECRET_KEY
    app.config.from_mapping(DEBUG=True)  # Activar modo debug

    # Métodos de validación:
    def validar_entrada(texto):
        # a-z y A-Z son para minusculas y mayusculas
        # \u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00c1\u00c9\u00cd\u00d3\u00da\u00d1  Letras mayusculas y minusculas con acentos
        # \s Espacios en blanco
        # '' Al menos un caracter del conjunto
        # $ Al final de la cadena
        # Definimos el patrón que NO queremos en la entrada
        patron = r"^[a-zA-Z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00c1\u00c9\u00cd\u00d3\u00da\u00d1\s]+$"

        # Buscamos si hay alguna coincidencia en el texto
        if not re.search(patron, texto):
            return False
        else:
            return True
        
    from . import nutriologo_paciente
    app.register_blueprint(nutriologo_paciente.bp)
    
    from . import cliente
    app.register_blueprint(cliente.bp)

    from . import nutriologo
    app.register_blueprint(nutriologo.bp)
    from . import auth
    app.register_blueprint(auth.bp)

    # Ruta dinámica para archivos estáticos
    @app.route("/static/<path:path>")
    def send_static(path):
        return send_from_directory("static", path)

    # Ruta Principal
    @app.route("/")
    def index():
        return render_template("index.html")  # Asegúrate de devolver el render_template con el nombre correcto de la plantilla

    return app
