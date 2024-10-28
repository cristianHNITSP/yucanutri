from flask import Blueprint, request, session, flash, redirect, url_for, render_template
from werkzeug.security import check_password_hash
import Config  # Asegúrate de que esta importación sea correcta

bp = Blueprint('auth', __name__,url_prefix='/auth')

@bp.route('/iniciar_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if 'estado' in session and session['estado'] is True:
        if session.get('rol') == 'nutriologo':
            return redirect(url_for('nutriologo.salaNutriologo')) 
        if session.get('rol') == 'superusuario':
            return redirect(url_for('superusuario.sala_superusuario')) 
        if session.get('rol') == 'paciente':
            return redirect(url_for('nutriologo_paciente.index_informacion')) 
        else: 
            return render_template("inicio_sesion.html")
    
    if request.method == 'POST':
        correo = str(request.form['correo'])
        contraseña = str(request.form['contraseña'])

        # Inicializar rol como visitante
        session['rol'] = 'visitante'
        
        print(f"Correo almacenado en sesión: {correo}")

        try:
            usuario_info = Config.Read(
                """
                SELECT 
                    r.rol,
                    s.correo_electronico AS correo,
                    s.contrasena, 
                    s.estado_sesion
                FROM 
                    public.superusuario s
                INNER JOIN 
                    public.rol r ON s.id_rol_id_rol = r.id_rol
                WHERE 
                    s.correo_electronico = %s

                UNION ALL

                SELECT 
                    r.rol,
                    n.correo_electronico AS correo,
                    n.contrasena, 
                    n.estado_sesion
                FROM 
                    public.nutriologo n
                INNER JOIN 
                    public.rol r ON n.id_rol_id_rol = r.id_rol
                WHERE 
                    n.correo_electronico = %s

                UNION ALL

                SELECT 
                    r.rol,
                    p.correo_electronico[1] AS correo,
                    p.contrasena,
                    p.estado_sesion 
                FROM 
                    public.paciente p
                INNER JOIN 
                    public.rol r ON p.id_rol_id_rol = r.id_rol
                WHERE 
                    p.correo_electronico[1] = %s;
                """, 
                (correo, correo, correo)
            )

            print("Resultado de la consulta usuario_info:", usuario_info)
            if usuario_info:
                for user in usuario_info:
                    rol_usuario = user[0]
                    correo_usuario = user[1]
                    contrasena_usuario = user[2]
                    estado = user[3]

                    print(f"Rol: {rol_usuario}, Correo: {correo_usuario}, Contraseña: {contrasena_usuario}")

                    if estado:  # Si el estado_sesion es True, no permitir el inicio de sesión
                        flash('La sesión ya está activa. Por favor, cierra la sesión primero.', 'warning')
                        return redirect(url_for('inicio_sesion'))

                    if rol_usuario == 'paciente':
                        if check_password_hash(contrasena_usuario, contraseña):
                            session['rol'] = rol_usuario
                            session['correo'] = correo_usuario
                            session['estado'] = True
                            Config.CUD(
                                """
                                UPDATE public.paciente
                                SET 
                                    estado_sesion = True
                                WHERE 
                                    correo_electronico[1] = %s
                                """,
                                (correo_usuario,)
                            )
                            print("sesión activa")
                            flash(f'Inicio de sesión exitoso como {rol_usuario}', 'success')
                            return redirect(url_for('nutriologo_paciente.index_informacion'))
                        else:
                            print("Contraseña incorrecta (hash) para el paciente:", correo_usuario)
                            flash('Correo o contraseña incorrectos', 'danger')

                    elif rol_usuario in ['nutriologo', 'superusuario']:
                        if contrasena_usuario == contraseña:
                            session['rol'] = rol_usuario
                            session['correo'] = correo_usuario
                            session['estado'] = True
                            Config.CUD(
                                """
                                UPDATE public.nutriologo
                                SET 
                                    estado_sesion = True
                                WHERE 
                                    correo_electronico = %s
                                """,
                                (correo_usuario,)
                            )
                            print("sesión activa")
                            flash(f'Inicio de sesión exitoso como {rol_usuario}', 'success')

                            if rol_usuario == 'superusuario':
                                return redirect(url_for('superusuario.sala_superusuario'))
                            elif rol_usuario == 'nutriologo':
                                return redirect(url_for('nutriologo.salaNutriologo'))
                        else:
                            print("Contraseña incorrecta para el usuario:", correo_usuario)
                            flash('Correo o contraseña incorrectos', 'danger')
                
                print("Credenciales incorrectas")
            else:
                flash('Usuario no encontrado', 'warning')
                print("Usuario no encontrado en los roles")

        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            flash('Ha ocurrido un error al iniciar sesión. Por favor, inténtalo de nuevo.', 'danger')

    print("session: ")
    print(session)
    
    return render_template("inicio_sesion.html")


