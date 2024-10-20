from flask import Blueprint, request, session, flash, redirect, url_for, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash  # Importar para verificar hash
import Config  # Asegúrate de que esta importación sea correcta


bp = Blueprint('auth', __name__)

@bp.route('/iniciar_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        # Guardar en la sesión
        session['correo'] = correo
        session['contraseña'] = contraseña

        # Imprimir en la consola de Python
        print(f"Correo almacenado en sesión: {session['correo']}")
        print(f"Contraseña almacenada en sesión: {session['contraseña']}")

        # Convertir a string y preparar los parámetros
        params = (str(session['correo']),)

        try:
            # Verificar como superusuario
            seleccionar_superusuario = Config.Read(
                """
                SELECT * 
                FROM public.superusuario 
                WHERE correo_electronico = %s AND contrasena = %s
                """, 
                (params[0], str(session['contraseña']))  # Pasar contraseña en claro
            )

            if seleccionar_superusuario:
                print("Conexión a la base de datos exitosa como superusuario")
                flash('Inicio de sesión exitoso como superusuario', 'success')
                return redirect(url_for('nutriologo.salaNutriologo'))

            # Verificar como nutriologo
            seleccionar_nutriologo = Config.Read(
                """
                SELECT * 
                FROM public.nutriologo 
                WHERE correo_electronico = %s AND contrasena = %s
                """, 
                (params[0], str(session['contraseña']))  # Pasar contraseña en claro
            )

            if seleccionar_nutriologo:
                print("Conexión a la base de datos exitosa como nutriologo")
                flash('Inicio de sesión exitoso como nutriologo', 'success')
                return redirect(url_for('nutriologo.salaNutriologo'))

            # Verificar como paciente (con hash)
            seleccionar_paciente = Config.Read(
                """
                SELECT contrasena 
                FROM public.paciente 
                WHERE correo_electronico = %s
                """, 
                params
            )

            if seleccionar_paciente:
                # Suponiendo que seleccionas solo un paciente
                hash_contrasena = seleccionar_paciente[0][0]  # Obtener solo el hash de la contraseña

                # Verificar el hash de la contraseña
                if check_password_hash(hash_contrasena, contraseña):
                    print("Conexión a la base de datos exitosa como paciente")
                    flash('Inicio de sesión exitoso como paciente', 'success')
                    return redirect(url_for('nutriologo_paciente.index_informacion'))
                else:
                    flash('Correo o contraseña incorrectos', 'error')
                    print("Credenciales incorrectas")

            # Si no se encuentra ninguna credencial
            flash('Correo o contraseña incorrectos', 'error')
            print("Credenciales incorrectas")

        except UnicodeDecodeError as ude:
            print(f"<-------------------- Error de codificación: {ude} -------------------->")
            flash('Error de codificación en los datos ingresados. Por favor, inténtalo de nuevo.', 'error')
        except Exception as e:
            # Manejo de errores inesperados
            print(f"Error al conectar a la base de datos: {e}")
            flash('Ha ocurrido un error al iniciar sesión. Por favor, inténtalo de nuevo.', 'error')

    return render_template("inicio_sesion.html")
