from flask import Blueprint, render_template, session, redirect, url_for, flash

bp = Blueprint('cerrar_sesion', __name__, url_prefix='/cerrar_sesion')


@bp.route('/cerrar_sesion')
def cerrar_sesion():
    # Limpiar toda la sesión
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('auth.inicio_sesion'))
