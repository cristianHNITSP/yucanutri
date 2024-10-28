import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import Config as Config
from werkzeug.security import generate_password_hash
from datetime import date, datetime

bp = Blueprint('nutriologo', __name__, url_prefix='/nutriologo')


@bp.route('/registrar_cliente', methods=['GET', 'POST'])
def registrarPaciente():

    # Verificar si el usuario ha iniciado sesión y tiene permisos
    if 'rol' not in session or (session.get('rol') != 'nutriologo' and session.get('rol') != 'superusuario'):
        flash('Acceso denegado: Registrar clientes es solo para nutriologo, inicia sesión.',
              'danger')
        # Redirigir al login si no está autorizado
        return redirect(url_for('auth.inicio_sesion'))

    if request.method == 'POST':

        # Obtener los datos del formulario y convertir a string
        nombres = str(request.form['nombres']).strip().lower()  # Minusculas
        ap_paterno = str(request.form['apellido_paterno']).strip().lower()
        ap_materno = str(request.form['apellido_materno']).strip().lower()

        # Convertir la fecha a tipo de dato fecha de PostgreSQL
        fecha_nacimiento_str = str(request.form['fecha_nacimiento']).strip()
        try:
            fecha_nacimiento = datetime.strptime(
                fecha_nacimiento_str, '%Y-%m-%d').date()

            # Verificar que la persona haya nacido en 2015 o antes
            if fecha_nacimiento.year > 2015:
                flash(
                    'Edad mínima de registro: 9 años.', 'danger')
                return redirect(url_for('nutriologo.registrarPaciente'))

        except ValueError:
            flash('Formato de fecha incorrecto. Usa YYYY-MM-DD.', 'error')
            return redirect(url_for('nutriologo.registrarPaciente'))

        # Los demas datos
        sexo = str(request.form['sexo']).strip()
        correo_electronico = str(request.form['correo_electronico']).strip()
        contrasena = str(request.form['contrasena']).strip()

        # Obtener el número de teléfono del formulario y quitar espacios
        telefono_str = request.form['telefono'].strip()

        # Validar que el teléfono tenga exactamente 10 dígitos numéricos
        if not telefono_str.isdigit() or len(telefono_str) != 10:
            flash(
                'El número de teléfono debe ser exactamente 10 dígitos numéricos.', 'error')
            return redirect(url_for('nutriologo.registrarPaciente'))

        # Convertir el teléfono a entero
        try:
            telefono = int(telefono_str)
            if telefono < 0:
                raise ValueError("El teléfono no puede ser negativo.")
        except ValueError:
            flash('Número de teléfono debe ser un entero positivo.', 'error')
            return redirect(url_for('nutriologo.registrarPaciente'))

        # generar contraseña hasheada
        contrasena_encriptada = generate_password_hash(contrasena)

        try:
            # Consulta para obtener el ID del nutriologo
            nutriologo_result = Config.Read(
                """
                SELECT id_nutriologo
                FROM public.nutriologo
                LIMIT 1
                """
            )

            if nutriologo_result:
                id_nutriologo_id_nutriologo = int(nutriologo_result[0][0])
                if id_nutriologo_id_nutriologo <= 0:
                    flash('ID de nutriologo no válido.', 'error')
                    return redirect(url_for('nutriologo.registrarPaciente'))

                # Verificar que el rol "paciente" existe y obtener su ID
                rol_result = Config.Read(
                    """
                    SELECT id_rol
                    FROM public.rol
                    WHERE rol = 'paciente'
                    LIMIT 1
                    """
                )

                if rol_result:
                    id_rol_id_rol = rol_result[0][0]

                    # Agregar el valor para status
                    status = True  # Se puede cambiar a False si necesitas que el paciente esté inactivo al principio

                    params = (
                        nombres,
                        ap_paterno,
                        ap_materno,
                        fecha_nacimiento,
                        sexo,
                        [correo_electronico],  # Cambiar a array
                        contrasena_encriptada,
                        telefono,
                        status,  # Agregar el estado aquí
                        id_rol_id_rol,  # Usar el ID del rol paciente
                        id_nutriologo_id_nutriologo
                    )

                    # Añadir esto para depuración
                    print(f"Datos a insertar: {params}")

                    # Insertar el paciente en la base de datos
                    Config.CUD(
                        """
                        INSERT INTO public.paciente
                        (nombres, ap_paterno, ap_materno, fecha_nacimiento, sexo, correo_electronico,
                         contrasena, telefono, status, id_rol_id_rol, id_nutriologo_id_nutriologo)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        params
                    )

                    flash('Paciente registrado exitosamente', 'success')

                    return redirect(url_for('nutriologo.salaNutriologo'))

                else:
                    flash('El rol "paciente" no existe en la base de datos.', 'error')

            else:
                flash(
                    'No se encontró ningún nutriologo. Por favor, verifica la base de datos.', 'error')

        except Exception as e:
            print(f"Error al registrar el paciente: {e}")
            flash(
                'Ha ocurrido un error al registrar el paciente. Por favor, inténtalo de nuevo.', 'error')

    return render_template("registrar_cliente.html")


# buscador por correo
@bp.route('/sala_nutriologo', methods=['GET', 'POST'])
def salaNutriologo():

    # Verificar si el usuario ha iniciado sesión y tiene permisos
    if 'rol' not in session or (session.get('rol') != 'nutriologo' and session.get('rol') != 'superusuario'):
        flash('Acceso denegado: La sala es solo para nutriologo, inicia sesión.', 'danger')
        return redirect(url_for('auth.inicio_sesion'))

    if request.method == 'POST':
        # Capturar el correo electrónico del formulario
        patient_email = request.form.get('patientEmail')

        # Validar que el campo del correo esté lleno
        if not patient_email:
            flash("El campo de correo electrónico es obligatorio.", "error")
            # Redirigir a la misma página
            return redirect(url_for('nutriologo.salaNutriologo'))

        # Realizar la consulta para buscar el paciente y su rol
        try:
            paciente_info = Config.Read(
                """
                SELECT
                    p.id_paciente,
                    p.nombres,
                    p.ap_paterno,
                    p.ap_materno,
                    p.fecha_nacimiento,
                    p.sexo,
                    p.correo_electronico[1] AS correo,
                    r.rol
                FROM
                    public.paciente p
                INNER JOIN
                    public.rol r ON p.id_rol_id_rol = r.id_rol
                WHERE
                    p.correo_electronico[1] = %s AND
                    p.status = true;  -- Solo buscar pacientes activos
                """,
                (patient_email,)  # Usar el correo como parámetro
            )
        except Exception as e:
            flash(f"Error al consultar la base de datos: {e}", "error")
            # Redirigir a la misma página
            return redirect(url_for('nutriologo.salaNutriologo'))

        # Comprobar si se encontró al paciente
        if not paciente_info:
            flash(
                "No se encontró un paciente con el correo proporcionado o está inactivo.", "error")
            # Redirigir a la misma página
            return redirect(url_for('nutriologo.salaNutriologo'))

        # Si se encontró al paciente, guardar los datos en la sesión (opcional)
        session['paciente_info'] = paciente_info[0]  # Guardar en la sesión
        print(f"Datos guardados en la sesión: {session['paciente_info']}")

        # Redirigir a 'nutriologo_paciente.index_informacion' con los datos del paciente
        return redirect(url_for('nutriologo_paciente.index_informacion'))

    # Si el método es GET, simplemente renderiza la plantilla
    return render_template("sala_nutriologo.html")


@bp.route('/cerrar_sesion_paciente')
def cerrar_sesion_paciente():
    # Limpiar solo la clave 'paciente_info' de la sesión
    session.pop('paciente_info', None)

    # Puedes redirigir a otra página después de limpiar la sesión
    flash('Has cerrado la sesión del paciente correctamente.', 'success')
    return redirect(url_for('nutriologo.salaNutriologo'))


@bp.route('/editar_datos_nutriologo')
def editar_datos_nutriologo():
    correo_nutriologo = session.get('correo', None)
    print("El correo en sesión es:", correo_nutriologo)

    # Verificar si el correo está en la sesión
    if correo_nutriologo is None:
        flash("No se ha encontrado el correo en la sesión.", "error")
        return redirect(url_for('nutriologo.salaNutriologo'))

    # Obtener los datos del nutriologo para mostrar
    try:
        nutriologo_info = Config.Read(
            """
            SELECT
                id_nutriologo,
                nombres,
                ap_paterno,
                ap_materno,
                telefono,
                correo_electronico,
                contrasena
            FROM
                nutriologo
            WHERE
                correo_electronico = %s;  -- Traer datos del nutriologo por correo
            """,
            (correo_nutriologo,)  # Usar el correo como parámetro
        )
    except Exception as e:
        flash(f"Error al consultar la base de datos: {e}", "error")
        return redirect(url_for('nutriologo.salaNutriologo'))

    print("Información del nutriólogo:", nutriologo_info)

    # Comprobar si se encontró al nutriólogo
    if not nutriologo_info:
        flash("No se encontró el nutriólogo.", "error")
        return redirect(url_for('nutriologo.salaNutriologo'))

    # Pasar la información correctamente a la plantilla
    return render_template("editar_nutriologo.html", dato=nutriologo_info[0])


@bp.route('/actualizar_nutriologo', methods=['POST'])
def actualizar_nutriologo():

    if request.method == 'POST':
        nombres = str(request.form['nombres']).strip().lower()  # Minusculas
        ap_paterno = str(request.form['apellido_p']).strip().lower()
        ap_materno = str(request.form['apellido_m']).strip().lower()
        telefono = str(request.form['telefono']).strip().lower()
        correo = str(request.form['correo']).strip().lower()
        contraseña = str(request.form['contraseña']).strip().lower()
        indice_id = str(request.form['indice_id']).strip().lower()

        # Validar que el correo electrónico termine en ".com"
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[cC][oO][mM]$", correo):
            flash("El correo electrónico debe terminar en '.com'", "error_email")
            return redirect(url_for('editar_perfil'))

        # Comprobar si el correo ya está registrado
        # cur.execute(
        #     "SELECT * FROM login WHERE Correo = %s AND ID_Login != %s", (correo, id))
        # existing_email = cur.fetchone()

        # Comprobar si el correo ya está registrado
        try:
            correo_ya_existe = Config.Read(
                """
                SELECT
                    *
                FROM
                    nutriologo
                WHERE
                    correo_electronico = %s;
                    AND id_nutriologo != %s;
                """,
                (correo, indice_id)  # Usar el correo como parámetro
            )
            telefono_ya_existe = Config.Read(
                """
                SELECT
                    *
                FROM
                    nutriologo
                WHERE
                    telefono = %s;
                    AND id_nutriologo != %s;
                """,
                (telefono, indice_id)  # Usar el correo como parámetro
            )
        except Exception as e:
            flash(f"Error al consultar la base de datos: {e}", "error")
            return redirect(url_for('nutriologo.editar_datos_nutriologo'))

        # Comprobar si el usuario ya existe
        # cur.execute(
        #     "SELECT * FROM login WHERE Nombre = %s AND ID_Login != %s", (user, id))
        # existing_user = cur.fetchone()

        if correo_ya_existe:
            flash("El correo electrónico ya está registrado", "error_email")
            return redirect(url_for('nutriologo.editar_datos_nutriologo'))

        elif telefono_ya_existe:
            flash("El telefono ya existe. Por favor, elija otro", "error_cel")
            return redirect(url_for('nutriologo.editar_datos_nutriologo'))

        else:
            # Actualizar los datos del usuario
            # cur.execute(
            #     "UPDATE login SET Nombre = %s, Correo = %s, Contraseña = %s WHERE ID_Login = %s",
            #     (user, correo, contraseña, id)
            # )

            try:
                Config.CUD(
                    """
                    UPDATE
                        nutriologo
                    SET
                        nombres = %s,
                        ap_paterno = %s,
                        ap_materno = %s,
                        telefono = %s,
                        correo_electronico = %s,
                        contrasena = %s
                    WHERE
                        id_nutriologo = %s
                    """,
                    (nombres, ap_paterno, ap_materno, telefono, correo,
                     contraseña, indice_id)  # Usar el correo como parámetro
                )
            except Exception as e:
                flash(f"Error al consultar la base de datos: {e}", "error")
                return redirect(url_for('nutriologo.editar_datos_nutriologo'))
            # Actualizar la sesión
            session["email"] = correo
            flash("Perfil editado correctamente", "perfil_editado")
            return redirect(url_for('nutriologo.editar_datos_nutriologo'))

    return redirect(url_for('nutriologo.editar_datos_nutriologo'))
