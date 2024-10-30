from flask import Blueprint, request, session, flash, redirect, url_for, render_template
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

@bp.route('/tiempo_de_inactividad', methods=['GET'])
def tiempo_de_inactividad():
    # Tu lógica para manejar el cierre de sesión
    try:
        # Verificamos si el usuario está en sesión y su estado es True
        if 'estado' in session and session['estado']:
            correo = session.get('correo')  # Recuperamos el correo del usuario
            rol = session.get('rol')  # Supongamos que el rol también está almacenado en la sesión
            
            # Imprimimos el estado y correo para fines de depuración
            print(session['estado'])
            print(correo)

            # Lógica para manejar el cierre de sesión según el rol
            if rol == 'nutriologo':
                Config.CUD(
                    """
                    UPDATE public.nutriologo
                    SET 
                        estado_sesion = False
                    WHERE 
                        correo_electronico = %s
                    """,
                    (correo,)
                )
            elif rol == 'paciente':
                Config.CUD(
                    """
                    UPDATE public.paciente
                    SET 
                        estado_sesion = False
                    WHERE 
                        correo_electronico = %s
                    """,
                    (correo,)
                )
            else:
                flash('Rol de usuario no reconocido.', 'warning')
                return redirect(url_for('auth.inicio_sesion'))

            # Limpiar la sesión
            session.clear()
            flash('Sesión cerrada correctamente.', 'success')
            return redirect(url_for('auth.inicio_sesion'))
        else:
            flash('La sesión no se cerró correctamente.', 'warning')
            return redirect(url_for('auth.inicio_sesion'))
    except Exception as e:
        flash(f'Ocurrió un error: {str(e)}', 'danger')
        return redirect(url_for('auth.inicio_sesion'))

@bp.route('/cerrar_sesion_todos_dispositivos', methods=['POST'])
def cerrar_sesion_todos_dispositivos():
    correo = request.form.get('correo')  # Obtén el correo del formulario
    # Inicializar rol como visitante
    session['rol'] = 'visitante'
    print('Se cammbio se sesion a ', (session['rol'])
 )
    
    # Verificar si el correo está vacío
    if not correo or not isinstance(correo, str):
        flash("El correo no puede estar vacío y debe ser un texto válido.", "error")  # Mensaje de error
        return redirect(url_for('auth.inicio_sesion'))  # Redirigir sin hacer nada

    # Aquí deberías conectar a tu base de datos y ejecutar la consulta de actualización
    try:
        Config.CUD(
            """
            UPDATE public.superusuario SET estado_sesion = FALSE WHERE correo_electronico = %s;
            UPDATE public.nutriologo SET estado_sesion = FALSE WHERE correo_electronico = %s;
            UPDATE public.paciente SET estado_sesion = FALSE WHERE correo_electronico[1] = %s;
            """, 
            (correo, correo, correo)
        )
        flash("Se cerraron las sesiones exitosamente.", "success")  # Mensaje flash
        session.clear()
    except Exception as e:
        flash("Error al cerrar las sesiones: {}".format(str(e)), "error")  # Manejo de errores

    return redirect(url_for('auth.inicio_sesion'))

