from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import Config as Config
from werkzeug.security import generate_password_hash


bp = Blueprint('nutriologo_paciente', __name__, url_prefix='/nutriologo_paciente')


@bp.route('/index_informacion')
def index_informacion():
    paciente_info = session.get('paciente_info')
    print(f"Datos del paciente actual: {paciente_info}")
    return render_template("index_informacion.html",)
