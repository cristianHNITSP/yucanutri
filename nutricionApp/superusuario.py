from flask import Blueprint, render_template, session

bp = Blueprint('superusuario', __name__, url_prefix='/superusuario')


@bp.route('/sala_superusuario')
def sala_superusuario():
    return render_template("superadmin.html")
