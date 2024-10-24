from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import Config as Config
from werkzeug.security import generate_password_hash
from datetime import datetime

bp = Blueprint('nutriologo', __name__, url_prefix='/nutriologo')

@bp.route('/registrar_cliente', methods=['GET', 'POST'])
def registrarPaciente():
    if request.method == 'POST':
        # Obtener los datos del formulario y convertir a string
        nombres = str(request.form['nombres']).strip()
        ap_paterno = str(request.form['apellido_paterno']).strip()
        ap_materno = str(request.form['apellido_materno']).strip()
        
        # Convertir la fecha a tipo de dato fecha de PostgreSQL
        fecha_nacimiento_str = str(request.form['fecha_nacimiento']).strip()
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha incorrecto. Usa YYYY-MM-DD.', 'error')
            return redirect(url_for('nutriologo.registrarPaciente'))
        
        sexo = str(request.form['sexo']).strip()
        correo_electronico = str(request.form['correo_electronico']).strip()
        contrasena = str(request.form['contrasena']).strip()
        
        # Convertir el teléfono a entero
        try:
            telefono = int(request.form['telefono'].strip())
            if telefono < 0:
                raise ValueError("El teléfono no puede ser negativo.")
        except ValueError:
            flash('Número de teléfono debe ser un entero positivo.', 'error')
            return redirect(url_for('nutriologo.registrarPaciente'))
        
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

                    print(f"Datos a insertar: {params}")  # Añadir esto para depuración

                    # Insertar el paciente en la base de datos
                    Config.CUD(
                        """
                        INSERT INTO public.paciente 
                        (nombres, ap_paterno, ap_materno, fecha_nacimiento, sexo, correo_electronico, contrasena, telefono, status, id_rol_id_rol, id_nutriologo_id_nutriologo)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, 
                        params
                    )

                    flash('Paciente registrado exitosamente', 'success')
                    return redirect(url_for('nutriologo.salaNutriologo'))

                else:
                    flash('El rol "paciente" no existe en la base de datos.', 'error')

            else:
                flash('No se encontró ningún nutriologo. Por favor, verifica la base de datos.', 'error')

        except Exception as e:
            print(f"Error al registrar el paciente: {e}")
            flash('Ha ocurrido un error al registrar el paciente. Por favor, inténtalo de nuevo.', 'error')

    return render_template("registrar_cliente.html")

@bp.route('/sala_nutriologo', methods=['GET', 'POST'])
def salaNutriologo():
    if request.method == 'POST':
        # Capturar el correo electrónico del formulario
        patient_email = request.form.get('patientEmail')

        # Validar que el campo del correo esté lleno
        if not patient_email:
            flash("El campo de correo electrónico es obligatorio.", "error")
            return redirect(url_for('nutriologo.salaNutriologo'))  # Redirigir a la misma página

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
            return redirect(url_for('nutriologo.salaNutriologo'))  # Redirigir a la misma página

        # Comprobar si se encontró al paciente
        if not paciente_info:
            flash("No se encontró un paciente con el correo proporcionado o está inactivo.", "error")
            return redirect(url_for('nutriologo.salaNutriologo'))  # Redirigir a la misma página

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
