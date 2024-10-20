from flask import Blueprint, render_template

import Config

bp = Blueprint('nutriologo', __name__, url_prefix='/nutriologo')

@bp.route('/iniciar_sesion')
def login():
    #{{ url_for('iniciar_sesion') }}
    return render_template ("inicio_sesion.html")

@bp.route('/registrar_cliente')
def registrar():
    return render_template("registrar_cliente.html")

