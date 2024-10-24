from flask import Blueprint, request, session, flash, redirect, url_for, render_template
from werkzeug.security import check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import Config  # Asegúrate de que esta importación sea correcta

bp = Blueprint('auth', __name__,url_prefix='/auth')

@bp.route('/iniciar_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        correo = str(request.form['correo'])
        contraseña = str(request.form['contraseña'])

        # Inicializar rol por defecto como visitante
        session['rol'] = 'visitante'
        
        # Imprimir en la consola de Python
        print(f"Correo almacenado en sesión: {correo}")

        try:
            # Realizar la consulta para recuperar el rol, correo y contraseña del usuario
            usuario_info = Config.Read(
                """
                SELECT 
                    r.rol,
                    s.correo_electronico AS correo,
                    s.contrasena 
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
                    n.contrasena 
                FROM 
                    public.nutriologo n
                INNER JOIN 
                    public.rol r ON n.id_rol_id_rol = r.id_rol
                WHERE 
                    n.correo_electronico = %s

                UNION ALL

                SELECT 
                    r.rol,
                    p.correo_electronico[1] AS correo,  -- Si `correo_electronico` es un array
                    p.contrasena 
                FROM 
                    public.paciente p
                INNER JOIN 
                    public.rol r ON p.id_rol_id_rol = r.id_rol
                WHERE 
                    p.correo_electronico[1] = %s;  -- Asumiendo que estamos usando el primer correo
                """, 
                (correo, correo, correo)  # Pasar el correo tres veces para las condiciones
            )

            # Depurar el resultado de la consulta
            print("Resultado de la consulta usuario_info:", usuario_info)

            if usuario_info:
                # Verificar la contraseña de acuerdo al rol
                for user in usuario_info:
                    rol_usuario = user[0]
                    correo_usuario = user[1]
                    contrasena_usuario = user[2]

                    # Imprimir información del usuario
                    print(f"Rol: {rol_usuario}, Correo: {correo_usuario}, Contraseña: {contrasena_usuario}")

                    # Si el rol es 'paciente', comparamos la contraseña usando check_password_hash
                    if rol_usuario == 'paciente':
                        if check_password_hash(contrasena_usuario, contraseña):
                            session['rol'] = rol_usuario
                            session['correo'] = correo_usuario  # Guardar correo en sesión
                            print(f"Inicio de sesión exitoso como {rol_usuario}. Rol: {session['rol']}")
                            flash(f'Inicio de sesión exitoso como {rol_usuario}', 'success')
                            return redirect(url_for('nutriologo_paciente.index_informacion'))
                        else:
                            print("Contraseña incorrecta (hash) para el paciente:", correo_usuario)
                            flash('Correo o contraseña incorrectos', 'error')

                    # Para 'nutriologo' y 'superusuario', compararemos la contraseña directamente (texto plano)
                    elif rol_usuario in ['nutriologo', 'superusuario']:
                        if contrasena_usuario == contraseña:
                            session['rol'] = rol_usuario
                            session['correo'] = correo_usuario  # Guardar correo en sesión
                            print(f"Inicio de sesión exitoso como {rol_usuario}. Rol: {session['rol']}")
                            flash(f'Inicio de sesión exitoso como {rol_usuario}', 'success')

                            # Redirigir según el rol
                            if rol_usuario == 'superusuario':
                                return redirect(url_for('superusuario.sala_superusuario'))
                            elif rol_usuario == 'nutriologo':
                                return redirect(url_for('nutriologo.salaNutriologo'))
                        else:
                            print("Contraseña incorrecta para el usuario:", correo_usuario)
                            flash('Correo o contraseña incorrectos', 'error')
                
                # Si no se ha encontrado un match en los roles o contraseñas
                print("Credenciales incorrectas")
            else:
                flash('Usuario no encontrado', 'error')
                print("Usuario no encontrado en los roles")

        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            flash('Ha ocurrido un error al iniciar sesión. Por favor, inténtalo de nuevo.', 'error')

    return render_template("inicio_sesion.html")
