from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import Config as Config
from werkzeug.security import generate_password_hash
from datetime import datetime



bp = Blueprint('nutriologo_paciente', __name__, url_prefix='/nutriologo_paciente')


@bp.route('/index_informacion')
def index_informacion():
    # Verificar si el rol está en la sesión
    rol = session.get('rol')
    if not rol:
        flash('Debes iniciar sesión para acceder a esta página.', 'error')
        # Redirige a la página de inicio de sesión
        return redirect(url_for('auth.inicio_sesion'))

    # Paso 1: Obtener el ID del paciente desde la sesión
    # Suponiendo que paciente_info ya está guardado
    paciente_info = session.get('paciente_info')
    if not paciente_info:
        print("Error: No se encontró información del paciente en la sesión.")
        flash('No se encontró información del paciente.', 'error')
        return render_template("index_informacion.html")

    # Extraemos el ID del paciente (primer elemento)
    id_paciente = paciente_info[0]
    print(f"ID del paciente obtenido: {id_paciente}")

    # Paso 2: Realizar la consulta para obtener el registro más reciente de progreso
    Consultar_el_progreso_mas_reciente = """
        SELECT 
            p.id_progreso,
            p.peso,
            p.abdomen,
            p.brazo_der_relajado,
            p.brazo_der_contraido,
            p.brazo_izq_relajado,
            p.brazo_izq_contraido,
            p.pierna_der_relajada,
            p.pierna_der_contraida,
            p.pierna_izq_relajada,
            p.pierna_izq_contraida,
            p.pantorrilla,
            p.porcentaje_grasa,
            p.porcentaje_musculo,
            d.dia AS dia_progreso,
            m.mes AS mes_progreso,
            a.anio AS anio_progreso
        FROM 
            public.progreso p
        INNER JOIN 
            public.dia_progreso d ON p.id_dia_progreso_id_dia = d.id_dia
        INNER JOIN 
            public.mes_progreso m ON p.id_mes_progreso_id_mes = m.id_mes
        INNER JOIN 
            public.anio_progreso a ON p.id_anio_progreso_id_anio = a.id_anio
        WHERE 
            p.id_paciente_paciente = %s
        ORDER BY 
            a.anio DESC, m.mes DESC, d.dia DESC  -- Ordena por año, mes y día en orden descendente
        LIMIT 1;  -- Limitamos a 1 para obtener el más reciente
        """

    Consultar_los_4_progresos_mas_recientes = """
        SELECT 
            p.id_progreso,
            p.peso,
            p.abdomen,
            p.brazo_der_relajado,
            p.brazo_der_contraido,
            p.brazo_izq_relajado,
            p.brazo_izq_contraido,
            p.pierna_der_relajada,
            p.pierna_der_contraida,
            p.pierna_izq_relajada,
            p.pierna_izq_contraida,
            p.pantorrilla,
            p.porcentaje_grasa,
            p.porcentaje_musculo,
            d.dia AS dia_progreso,
            m.mes AS mes_progreso,
            a.anio AS anio_progreso
        FROM 
            public.progreso p
        INNER JOIN 
            public.dia_progreso d ON p.id_dia_progreso_id_dia = d.id_dia
        INNER JOIN 
            public.mes_progreso m ON p.id_mes_progreso_id_mes = m.id_mes
        INNER JOIN 
            public.anio_progreso a ON p.id_anio_progreso_id_anio = a.id_anio
        WHERE 
            p.id_paciente_paciente = %s
        ORDER BY 
            a.anio DESC, m.mes DESC, d.dia DESC  -- Ordenamos por fecha más reciente
        LIMIT 4;  -- Limitar a los 4 registros más recientes
        """

    # Paso 3: Ejecutar la consulta
    try:
        # Llamamos a Config.Read pasándole el ID del paciente
        registro_progreso = Config.Read(
            Consultar_el_progreso_mas_reciente, (id_paciente,))
        print(f"Consulta ejecutada con éxito para el paciente ID: {
              id_paciente}")

        # Depurar el resultado de la consulta
        print("Resultado de la consulta registro_progreso:", registro_progreso)
        print(f"Contenido de session:", dict(session))

        if registro_progreso:
            # Paso 4: Obtener el primer registro de progreso
            datos_progreso = registro_progreso[0]
            print("Registro más reciente de progreso del paciente:")
            print(datos_progreso)  # Imprimir datos de progreso en la consola
            # Paso 5: Pasar los datos a la plantilla
            return render_template("index_informacion.html", paciente_info=paciente_info, progreso=datos_progreso)
        else:
            print(
                "Advertencia: No se encontraron registros de progreso para este paciente.")
            flash(
                'No se encontraron registros de progreso para este paciente.', 'warning')
            return render_template("index_informacion.html", paciente_info=paciente_info)

    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        flash('Ha ocurrido un error al recuperar la información del progreso. Por favor, inténtalo de nuevo.', 'error')
        return render_template("index_informacion.html", paciente_info=paciente_info)

@bp.route('/crear_nuevo_progreso', methods=['POST'])
def crear_nuevo_progreso():
    try:
        # Obtención de datos y validación de que son numéricos
        peso = float(request.form.get('peso', 0))
        abdomen = float(request.form.get('abdomen', 0))
        brazo_der_relajado = float(request.form.get('brazo_der_relajado', 0))
        brazo_der_contraido = float(request.form.get('brazo_der_contraido', 0))
        brazo_izq_relajado = float(request.form.get('brazo_izq_relajado', 0))
        brazo_izq_contraido = float(request.form.get('brazo_izq_contraido', 0))
        pierna_der_relajada = float(request.form.get('pierna_der_relajada', 0))
        pierna_der_contraida = float(request.form.get('pierna_der_contraida', 0))
        pierna_izq_relajada = float(request.form.get('pierna_izq_relajada', 0))
        pierna_izq_contraida = float(request.form.get('pierna_izq_contraida', 0))
        pantorrilla = float(request.form.get('pantorrilla', 0))
        porcentaje_grasa = float(request.form.get('porcentaje_grasa', 0))
        porcentaje_musculo = float(request.form.get('porcentaje_musculo', 0))

        # Validación de valores positivos
        if any(value <= 0 for value in [peso, abdomen, brazo_der_relajado, brazo_der_contraido,
                                        brazo_izq_relajado, brazo_izq_contraido,
                                        pierna_der_relajada, pierna_der_contraida,
                                        pierna_izq_relajada, pierna_izq_contraida,
                                        pantorrilla, porcentaje_grasa, porcentaje_musculo]):
            flash('Ha ingresado un valor invalido, intentelo nuevamente.', 'error')
            return redirect(url_for('nutriologo_paciente.index_informacion'))

        # Verificación de información del paciente
        paciente_info = session.get('paciente_info')
        if not paciente_info or len(paciente_info) == 0:
            flash('No se encontró información del paciente.', 'error')
            return redirect(url_for('nutriologo_paciente.index_informacion'))

        # Obtener el id del paciente
        id_paciente = paciente_info[0]
        print(f'ID Paciente: {id_paciente}')  # Debug: mostrar ID del paciente

        # Obtención de la fecha actual
        fecha_actual = datetime.now()
        dia = fecha_actual.day
        mes = fecha_actual.month
        anio = fecha_actual.year
        print(f'Fecha Actual: {dia}-{mes}-{anio}')  # Debug: mostrar fecha actual

        # Validación de la fecha
        try:
            fecha_validada = datetime(anio, mes, dia)
        except ValueError as e:
            flash('La fecha obtenida es inválida.', 'error')
            print(f'Error de fecha: {e}')  # Mensaje de error para depuración
            return redirect(url_for('nutriologo_paciente.index_informacion'))

        # Diccionario de meses en español
        meses_espanol = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        
        # Obtener el mes en español
        mes_espanol = meses_espanol[mes]
        print(f'Mes en Español: {mes_espanol}')  # Debug: mostrar mes en español

        # Consulta para obtener IDs de día, mes y año
        consulta_ids = """
            SELECT 
                (SELECT id_dia FROM public.dia_progreso WHERE dia = %s) AS id_dia,
                (SELECT id_mes FROM public.mes_progreso WHERE mes = %s) AS id_mes,
                (SELECT id_anio FROM public.anio_progreso WHERE anio = %s) AS id_anio
        """
        ids_info = Config.Read(consulta_ids, (dia, mes_espanol, anio))
        print(f'IDs Info: {ids_info}')  # Debug: mostrar resultado de la consulta de IDs

        if not ids_info or len(ids_info) == 0:
            flash('No se pudo obtener los IDs de día, mes o año.', 'error')
            return redirect(url_for('nutriologo_paciente.index_informacion'))

        # Desempaquetar los resultados obtenidos
        id_dia, id_mes, id_anio = ids_info[0]
        print(f"ID Día: {id_dia}, ID Mes: {id_mes}, ID Año: {id_anio}")  # Debug: mostrar IDs obtenidos

        # Verificar si ya existe un progreso para la fecha actual y el paciente
        consulta_existente = """
            SELECT COUNT(*) FROM public.progreso 
            WHERE id_paciente_paciente = %s 
            AND id_dia_progreso_id_dia = %s 
            AND id_mes_progreso_id_mes = %s 
            AND id_anio_progreso_id_anio = %s
        """
        progreso_existente = Config.Read(consulta_existente, (id_paciente, id_dia, id_mes, id_anio))

        if progreso_existente[0][0] > 0:
            flash('Ya existe un progreso registrado para esta fecha.', 'error')
            return redirect(url_for('nutriologo_paciente.index_informacion'))

        # Datos a almacenar o procesar
        datos_progresos = {
            'peso': peso,
            'abdomen': abdomen,
            'brazo_der_relajado': brazo_der_relajado,
            'brazo_der_contraido': brazo_der_contraido,
            'brazo_izq_relajado': brazo_izq_relajado,
            'brazo_izq_contraido': brazo_izq_contraido,
            'pierna_der_relajada': pierna_der_relajada,
            'pierna_der_contraida': pierna_der_contraida,
            'pierna_izq_relajada': pierna_izq_relajada,
            'pierna_izq_contraida': pierna_izq_contraida,
            'pantorrilla': pantorrilla,
            'porcentaje_grasa': porcentaje_grasa,
            'porcentaje_musculo': porcentaje_musculo,
            'id_dia': id_dia,
            'id_mes': id_mes,
            'id_anio': id_anio,
            'id_paciente': id_paciente  # Agregar el id_paciente a los datos
        }

        # Imprimir datos para depuración
        print("Datos recibidos:")
        for key, value in datos_progresos.items():
            print(f"{key}: {value}")  # Debug: mostrar todos los datos recibidos

        # Consulta de inserción
        Agregar_datos_progresos = """
            INSERT INTO public.progreso (
                peso,
                abdomen,
                brazo_der_relajado,
                brazo_der_contraido,
                brazo_izq_relajado,
                brazo_izq_contraido,
                pierna_der_relajada,
                pierna_der_contraida,
                pierna_izq_relajada,
                pierna_izq_contraida,
                pantorrilla,
                porcentaje_grasa,
                porcentaje_musculo,
                id_paciente_paciente,
                id_dia_progreso_id_dia,
                id_mes_progreso_id_mes,
                id_anio_progreso_id_anio
            ) 
            VALUES (%(peso)s, %(abdomen)s, %(brazo_der_relajado)s, %(brazo_der_contraido)s,
                    %(brazo_izq_relajado)s, %(brazo_izq_contraido)s, %(pierna_der_relajada)s,
                    %(pierna_der_contraida)s, %(pierna_izq_relajada)s, %(pierna_izq_contraida)s,
                    %(pantorrilla)s, %(porcentaje_grasa)s, %(porcentaje_musculo)s,
                    %(id_paciente)s, %(id_dia)s, %(id_mes)s, %(id_anio)s)
        """

        # Llamar a la función para ejecutar la inserción
        Config.CUD(Agregar_datos_progresos, datos_progresos)
        print('Inserción completada exitosamente.')  # Debug: confirmación de inserción

    except ValueError as e:
        flash('Por favor, ingrese valores numéricos válidos.', 'error')
        print(f'Error de valor: {e}')  # Mensaje de error para depuración
        return redirect(url_for('nutriologo_paciente.index_informacion'))

    # Redirigir a la página de información del paciente
    flash('Progreso registrado exitosamente.', 'success')
    return redirect(url_for('nutriologo_paciente.index_informacion'))

@bp.route('/editar_progreso', methods=['POST'])
def editar_progreso():
    try:
        # Capturando el ID del progreso
        id_progreso = int(request.form.get('id_progreso', 0))

        # Capturando los datos del formulario
        peso = float(request.form.get('peso_edit', 0))
        abdomen = float(request.form.get('abdomen_edit', 0))
        brazo_der_relajado = float(request.form.get('brazo_der_relajado_edit', 0))
        brazo_der_contraido = float(request.form.get('brazo_der_contraido_edit', 0))
        brazo_izq_relajado = float(request.form.get('brazo_izq_relajado_edit', 0))
        brazo_izq_contraido = float(request.form.get('brazo_izq_contraido_edit', 0))
        pierna_der_relajada = float(request.form.get('pierna_der_relajada_edit', 0))
        pierna_der_contraida = float(request.form.get('pierna_der_contraida_edit', 0))
        pierna_izq_relajada = float(request.form.get('pierna_izq_relajada_edit', 0))
        pierna_izq_contraida = float(request.form.get('pierna_izq_contraida_edit', 0))
        pantorrilla = float(request.form.get('pantorrilla_edit', 0))
        porcentaje_grasa = float(request.form.get('porcentaje_grasa_edit', 0))
        porcentaje_musculo = float(request.form.get('porcentaje_musculo_edit', 0))

        print('el peso actual a editar es de: ', peso)

        # Validación de valores positivos
        if any(value <= 0 for value in [peso, abdomen, brazo_der_relajado, brazo_der_contraido,
                                         brazo_izq_relajado, brazo_izq_contraido,
                                         pierna_der_relajada, pierna_der_contraida,
                                         pierna_izq_relajada, pierna_izq_contraida,
                                         pantorrilla, porcentaje_grasa, porcentaje_musculo]):
            flash('Ha ingresado un valor invalido, intentelo nuevamente.', 'error')
            return redirect(url_for('nutriologo_paciente.index_informacion'))

        # Verificación de información del paciente
        paciente_info = session.get('paciente_info')
        if not paciente_info or len(paciente_info) == 0:
            flash('No se encontró información del paciente.', 'error')
            return redirect(url_for('nutriologo_paciente.index_informacion'))

        # Guardando los datos en un diccionario
        datos_editar_progresos = {
            'id_progreso': id_progreso,
            'peso': peso,
            'abdomen': abdomen,
            'brazo_der_relajado': brazo_der_relajado,
            'brazo_der_contraido': brazo_der_contraido,
            'brazo_izq_relajado': brazo_izq_relajado,
            'brazo_izq_contraido': brazo_izq_contraido,
            'pierna_der_relajada': pierna_der_relajada,
            'pierna_der_contraida': pierna_der_contraida,
            'pierna_izq_relajada': pierna_izq_relajada,
            'pierna_izq_contraida': pierna_izq_contraida,
            'pantorrilla': pantorrilla,
            'porcentaje_grasa': porcentaje_grasa,
            'porcentaje_musculo': porcentaje_musculo    
        }

        print("Los datos a actualiza son:", datos_editar_progresos)

        actualizar_datos_progresos = """
            UPDATE public.progreso
            SET 
                peso = %(peso)s,
                abdomen = %(abdomen)s,
                brazo_der_relajado = %(brazo_der_relajado)s,
                brazo_der_contraido = %(brazo_der_contraido)s,
                brazo_izq_relajado = %(brazo_izq_relajado)s,
                brazo_izq_contraido = %(brazo_izq_contraido)s,
                pierna_der_relajada = %(pierna_der_relajada)s,
                pierna_der_contraida = %(pierna_der_contraida)s,
                pierna_izq_relajada = %(pierna_izq_relajada)s,
                pierna_izq_contraida = %(pierna_izq_contraida)s,
                pantorrilla = %(pantorrilla)s,
                porcentaje_grasa = %(porcentaje_grasa)s,
                porcentaje_musculo = %(porcentaje_musculo)s
            WHERE id_progreso = %(id_progreso)s
        """
        
        # Actualizar los datos en la base de datos
        Config.CUD(actualizar_datos_progresos, datos_editar_progresos)
        print('Actualización completada exitosamente.')  # Debug: confirmación de actualización

    except Exception as e:
        flash(f'Ocurrió un error: {str(e)}', 'error')
        print(f'Error: {str(e)}')  # Debug: imprimir el error en la consola

    return redirect(url_for('nutriologo_paciente.index_informacion'))







