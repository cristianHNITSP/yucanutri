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
        
        rol = 'paciente'
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

                # Agregar el valor para status
                status = True  # Se puede cambiar a False si necesitas que el paciente esté inactivo al principio

                params = (
                    nombres,
                    ap_paterno,
                    ap_materno,
                    fecha_nacimiento,
                    sexo,
                    correo_electronico,
                    contrasena_encriptada,
                    rol,
                    telefono,
                    status,  # Agregar el estado aquí
                    id_nutriologo_id_nutriologo
                )

                print(f"Datos a insertar: {params}")  # Añadir esto para depuración

                # Insertar el paciente en la base de datos
                Config.CUD(
                    """
                    INSERT INTO public.paciente 
                    (nombres, ap_paterno, ap_materno, fecha_nacimiento, sexo, correo_electronico, contrasena, rol, telefono, status, id_nutriologo_id_nutriologo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, 
                    params
                )

                # Crear el rol en PostgreSQL utilizando el correo sin modificaciones
                Config.CUD("""CREATE ROLE "{}" WITH LOGIN PASSWORD '{}';""".format(correo_electronico, contrasena))  # Usar el correo tal cual

                # Otorgar permisos al nuevo rol
                grant_queries = [
                    f'GRANT SELECT, UPDATE ON public.paciente TO "{correo_electronico}";',
                    f'GRANT SELECT ON public.plan_alimenticio TO "{correo_electronico}";',
                    f'GRANT SELECT ON public.progreso TO "{correo_electronico}";',
                    f'GRANT SELECT ON public.rutina_de_ejercicio TO "{correo_electronico}";',
                    f'GRANT SELECT ON public.semana_plan_comida TO "{correo_electronico}";',
                    f'GRANT SELECT, UPDATE ON public.nutriologo TO "{correo_electronico}";',
                    f'GRANT SELECT ON public.mes TO "{correo_electronico}";',
                    f'GRANT SELECT ON public.dia TO "{correo_electronico}";',
                    f'GRANT SELECT ON public.anio TO "{correo_electronico}";',
                ]
                
                for query in grant_queries:
                    try:
                        print(f"Ejecutando consulta: {query}")  # Mostrar la consulta que se está ejecutando
                        Config.CUD(query)  # Ejecutar la consulta
                        print(f"Permisos otorgados con éxito para {correo_electronico}.")  # Mensaje de éxito
                    except Exception as e:
                        print(f"Error al otorgar permisos: {e}")  # Mostrar error en caso de fallo

                flash('Paciente registrado y rol creado exitosamente', 'success')
                return redirect(url_for('nutriologo.salaNutriologo'))

            else:
                flash('No se encontró ningún nutriologo. Por favor, verifica la base de datos.', 'error')

        except Exception as e:
            print(f"Error al registrar el paciente o crear rol: {e}")
            flash('Ha ocurrido un error al registrar el paciente. Por favor, inténtalo de nuevo.', 'error')

    return render_template("registrar_cliente.html")



@bp.route('/sala_nutriologo', methods=['GET', 'POST'])
def salaNutriologo():
    if request.method == 'POST':
        # Capturar los valores del formulario
        patient_name = request.form.get('patientName')
        father_surname = request.form.get('fatherSurname')
        mother_surname = request.form.get('motherSurname')
        patient_email = request.form.get('patientEmail')
        
        # Imprimir los valores en la consola
        print(f'Nombre del paciente: {patient_name}')
        print(f'Apellido Paterno: {father_surname}')
        print(f'Apellido Materno: {mother_surname}')
        print(f'Correo Electrónico: {patient_email}')
    
    return render_template("sala_nutriologo.html")

