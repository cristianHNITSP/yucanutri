from flask import Blueprint, render_template, session, redirect, url_for, flash
import Config 
bp = Blueprint('cerrar_sesion', __name__, url_prefix='/cerrar_sesion')


@bp.route('/cerrar_sesion')
def cerrar_sesion():
    # Limpiar toda la sesión
    print(session['estado'])
    print(session['correo'])
    if session['estado'] is True:
        Config.CUD(
        """
        UPDATE public.nutriologo
        SET 
        estado_sesion = False
        WHERE 
        correo_electronico = %s
        """,
            (session.get('correo'),)
        )
        session.clear()
        flash('Sesión cerrada correctamente.', 'success')
        return redirect(url_for('auth.inicio_sesion'))
    else:
        flash('La sesión no se cerró correctamente.', 'warning')
        return redirect(url_for('auth.inicio_sesion'))
