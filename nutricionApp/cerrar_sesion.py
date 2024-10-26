from flask import Blueprint, render_template, session, redirect, url_for, flash
import Config 
bp = Blueprint('cerrar_sesion', __name__, url_prefix='/cerrar_sesion')


@bp.route('/cerrar_sesion_nutriologo')
def cerrar_sesion_nutriologo():
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
    
@bp.route('/cerrar_sesion_paciente')
def cerrar_sesion_paciente():
    print(session['estado'])
    print(session['correo'])
    
    if session['estado'] is True:
        Config.CUD(
            """
            UPDATE public.paciente
            SET 
                estado_sesion = False
            WHERE 
                correo_electronico[1] = %s
            """,
            (session.get('correo'),)  # Pasa el correo como un array en la consulta
        )
        session.clear()
        flash('Sesión cerrada correctamente.', 'success')
        return redirect(url_for('auth.inicio_sesion'))
    else:
        flash('La sesión no se cerró correctamente.', 'warning')
        return redirect(url_for('auth.inicio_sesion'))

