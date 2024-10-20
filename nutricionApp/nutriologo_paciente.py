from flask import Blueprint, render_template

bp = Blueprint('nutriologo_paciente', __name__, url_prefix='/nutriologo_paciente')


@bp.route('/index_informacion')
def index_información():
    return render_template("index_informacion.html")
