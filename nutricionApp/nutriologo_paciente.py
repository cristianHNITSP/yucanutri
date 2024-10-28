from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import Config as Config
from werkzeug.security import generate_password_hash
from datetime import datetime

bp = Blueprint('nutriologo_paciente', __name__, url_prefix='/nutriologo_paciente')

@bp.route('/index_informacion')
def index_informacion():
    rol = session.get('rol')
    if not rol:
        flash('Debes iniciar sesión para acceder a esta página.', 'error')
        return redirect(url_for('auth.inicio_sesion'))
    
    paciente_info = None
    paciente_datos = []  # Inicializado como una lista vacía
    registro_progreso = []  # Cambiado a lista vacía
    registro_plan_alimenticio = []  # Cambiado a lista vacía
    has_plan_alimentacion = False
    plan_comidas_semanales = {"comidas": []}

    try:
        if rol == 'nutriologo':
            paciente_info = session.get('paciente_info')
            if not paciente_info:
                flash('No se encontró información del paciente.', 'error')
                return redirect(url_for('nutriologo.cambiar_paciente'))

            id_paciente = paciente_info[0]

        elif rol == 'paciente':
            correo_electronico = session.get('correo')
            if not correo_electronico:
                flash('No se encontró el correo electrónico.', 'error')
                return render_template("index_informacion.html", rol=rol, has_plan_alimentacion=has_plan_alimentacion, plan_comidas_semanales=plan_comidas_semanales)

            Consultar_datos_paciente = """
                SELECT 
                    id_paciente, 
                    nombres, 
                    ap_paterno, 
                    ap_materno, 
                    fecha_nacimiento, 
                    sexo, 
                    telefono
                FROM 
                    public.paciente 
                WHERE 
                    %s = ANY(correo_electronico)
            """
            paciente_datos = Config.Read(Consultar_datos_paciente, (correo_electronico,))
            
            if not paciente_datos:
                flash('No se encontraron datos del paciente.', 'warning')
                return render_template("index_informacion.html", rol=rol, has_plan_alimentacion=has_plan_alimentacion, plan_comidas_semanales=plan_comidas_semanales)

            id_paciente = paciente_datos[0][0]

        # Obtener datos del paciente, progreso y plan alimenticio
        registro_progreso, registro_plan_alimenticio = obtener_datos_paciente(id_paciente)

        # Verificar si hay datos de progreso
        if not registro_progreso:
            flash('No se encontraron datos de progreso para este paciente.', 'warning')

        # Verificar si hay datos del plan alimenticio
        if not registro_plan_alimenticio:
            flash('No se encontraron datos del plan alimenticio para este paciente.', 'warning')

        # Asegúrate de que registro_progreso y registro_plan_alimenticio no estén vacíos antes de acceder a sus elementos
        datos_progreso = registro_progreso[0] if registro_progreso else None
        datos_planes_alimenticios = registro_plan_alimenticio if registro_plan_alimenticio else None

        if datos_planes_alimenticios:
            has_plan_alimentacion = True
            id_plan_alimenticio = datos_planes_alimenticios[0][0]

            # Obtener el plan de comidas semanales
            try:
                plan_comidas_semanales = obtener_plan_comidas_semanal_paciente(id_plan_alimenticio)
                if not plan_comidas_semanales.get("comidas"):
                    flash('No se encontró el plan de comidas semanales.', 'warning')
            except Exception as e:
                print(f"Error al obtener el plan de comidas: {e}")
                flash('Error al recuperar el plan de comidas, se devolverá una lista vacía.', 'warning')
                plan_comidas_semanales = {"comidas": []}  # Devuelve un dict con comidas vacías

        else:
            flash('No se encontraron planes alimenticios para este paciente.', 'warning')

        print('¿Se encontraron los planes alimenticios semanales?:', has_plan_alimentacion)   
        print('Datos del paciente actual: ', paciente_datos)    
        print('El progreso actual del paciente es: ', registro_progreso)
        print('El plan alimenticio es: ', registro_plan_alimenticio)
        print('El plan semanal de comida es: ', plan_comidas_semanales)

        return render_template("index_informacion.html", 
                                paciente_info=paciente_datos[0] if paciente_datos else paciente_info, 
                                progreso=datos_progreso, 
                                plan_alimenticio=datos_planes_alimenticios,
                                plan_comidas_semanales=plan_comidas_semanales,
                                has_plan_alimentacion=has_plan_alimentacion,  
                                rol=rol)

    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        flash('Ha ocurrido un error al recuperar la información. Por favor, inténtalo de nuevo.', 'error')
        return render_template("index_informacion.html", 
                                rol=rol, 
                                paciente_info=paciente_datos[0] if paciente_datos else paciente_info, 
                                has_plan_alimentacion=has_plan_alimentacion, 
                                plan_comidas_semanales=plan_comidas_semanales)




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
            flash('Ha ingresado un valor invalido, intentelo nuevamente.', 'warning')
            return redirect(url_for('nutriologo_paciente.index_informacion'))
        
                # Validar límites
        if peso > 700:
            flash('El peso no puede exceder los 700kg.', 'warning')
            return redirect(url_for('nutriologo_paciente.index_informacion'))
        
        if porcentaje_grasa > 70 or porcentaje_musculo > 70:
            flash('Los porcentajes de grasa y músculo no pueden exceder el 70%.', 'warning')
            return redirect(url_for('nutriologo_paciente.index_informacion'))
        
        medidas_brazos = [
            abdomen, brazo_der_relajado, brazo_der_contraido, brazo_izq_relajado, 
            brazo_izq_contraido
        ]
        
        medidas_piernas = [
            pierna_der_relajada, pierna_der_contraida, 
            pierna_izq_relajada, pierna_izq_contraida
        ]

                # Definimos las categorías de medidas y sus límites máximos, junto con el mensaje a mostrar
        categorias_medidas = [
            (medidas_brazos, 80, 'Las medidas referentes a brazos no pueden exceder los 80cm.'),
            (medidas_piernas, 120, 'Las medidas referentes a piernas no pueden exceder los 120cm.'),
            ([pantorrilla], 100, 'La medida de la pantorrilla no puede exceder los 100cm.')
        ]

        # Iteramos sobre cada categoría de medida, su límite y mensaje de error
        for medidas, limite, mensaje in categorias_medidas:
            if any(medida > limite for medida in medidas):
                flash(mensaje, 'warning')
                return redirect(url_for('nutriologo_paciente.index_informacion'))

        # Verificación de información del paciente
        paciente_info = session.get('paciente_info')
        if not paciente_info or len(paciente_info) == 0:
            flash('No se encontró información del paciente.', 'warning')
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
            flash('La fecha obtenida es inválida.', 'warning')
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
            flash('No se pudo obtener los IDs de día, mes o año.', 'warning')
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
            flash('Ya existe un progreso registrado para esta fecha.', 'warning')
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
        flash('Por favor, ingrese valores numéricos válidos.', 'warning')
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
            flash('Ha ingresado un valor invalido, intentelo nuevamente.', 'warning')
            return redirect(url_for('nutriologo_paciente.index_informacion'))
        
        if peso > 700:
            flash('El peso no puede exceder los 700kg.', 'warning')
            return redirect(url_for('nutriologo_paciente.index_informacion'))
        
        if porcentaje_grasa > 70 or porcentaje_musculo > 70:
            flash('Los porcentajes de grasa y músculo no pueden exceder el 70%.', 'warning')
            return redirect(url_for('nutriologo_paciente.index_informacion'))
        
        medidas_brazos = [
            abdomen, brazo_der_relajado, brazo_der_contraido, brazo_izq_relajado, 
            brazo_izq_contraido
        ]
        
        medidas_piernas = [
            pierna_der_relajada, pierna_der_contraida, 
            pierna_izq_relajada, pierna_izq_contraida
        ]

                # Definimos las categorías de medidas y sus límites máximos, junto con el mensaje a mostrar
        categorias_medidas = [
            (medidas_brazos, 80, 'Las medidas referentes a brazos no pueden exceder los 80cm.'),
            (medidas_piernas, 120, 'Las medidas referentes a piernas no pueden exceder los 120cm.'),
            ([pantorrilla], 100, 'La medida de la pantorrilla no puede exceder los 100cm.')
        ]

        # Iteramos sobre cada categoría de medida, su límite y mensaje de error
        for medidas, limite, mensaje in categorias_medidas:
            if any(medida > limite for medida in medidas):
                flash(mensaje, 'warning')
                return redirect(url_for('nutriologo_paciente.index_informacion'))

        # Verificación de información del paciente
        paciente_info = session.get('paciente_info')
        if not paciente_info or len(paciente_info) == 0:
            flash('No se encontró información del paciente.', 'warning')
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
        flash('Actualización completada exitosamente.', 'success')  #  
        print('Actualización completada exitosamente.')  # Debug: confirmación de actualización

    except Exception as e:
        flash(f'Ocurrió un error: {str(e)}', 'warning')
        print(f'Error: {str(e)}')  # Debug: imprimir el error en la consola

    return redirect(url_for('nutriologo_paciente.index_informacion'))

@bp.route('/agregar_nuevo_plan', methods=['POST'])
def agregar_nuevo_plan():
    # Obtener los datos del formulario con validación para campos requeridos
    alimento_permitido = request.form.get('low_calorie_foods', '').strip()
    comidas_evitar = request.form.get('avoid_foods', '').strip()
    bebidas_permitidas = request.form.get('allowed_drinks', '').strip()
    tips_alimentacion = request.form.get('nutrition_tips', '').strip() or "sin tips alimenticios"  # Usar "sin tips" si está vacío
    suplementos = request.form.get('supplement_details', '').strip() or "sin suplementos"  # Usar "sin suplementos" si está vacío

    tiempos_comida = request.form.getlist('tiempos_comida[]')

    max_length = 1000
    if (
        len(alimento_permitido) > max_length or
        len(comidas_evitar) > max_length or
        len(bebidas_permitidas) > max_length or
        len(tips_alimentacion) > max_length or
        len(suplementos) > max_length
    ):
        flash('Cada campo debe contener un máximo de 1000 caracteres.', 'warning')
        return redirect(url_for('nutriologo_paciente.index_informacion'))

    # Validar campos obligatorios
    if not alimento_permitido or not comidas_evitar or not bebidas_permitidas or len(tiempos_comida) < 5:
        flash('Por favor, complete todos los campos obligatorios.', 'warning')
        return redirect(url_for('nutriologo_paciente.index_informacion'))

    # Asignar los tiempos de comida
    tiempo_desayuno = tiempos_comida[0]
    tiempo_almuerzo = tiempos_comida[1]
    tiempo_durante_entrenamiento = tiempos_comida[2]
    tiempo_terminar_entrenar = tiempos_comida[3]
    tiempo_cena = tiempos_comida[4]

    # Menús para cada tiempo de comida
    menus = [
        {
            'tiempo': tiempo_desayuno,
            'menu1': request.form.get('menu1_desayuno', '').strip(),
            'menu2': request.form.get('menu2_desayuno', '').strip(),
            'menu3': request.form.get('menu3_desayuno', '').strip(),
        },
        {
            'tiempo': tiempo_almuerzo,
            'menu1': request.form.get('menu1_almuerzo', '').strip(),
            'menu2': request.form.get('menu2_almuerzo', '').strip(),
            'menu3': request.form.get('menu3_almuerzo', '').strip(),
        },
        {
            'tiempo': tiempo_durante_entrenamiento,
            'menu1': request.form.get('menu1_durante_entrenamiento', '').strip(),
            'menu2': request.form.get('menu2_durante_entrenamiento', '').strip(),
            'menu3': request.form.get('menu3_durante_entrenamiento', '').strip(),
        },
        {
            'tiempo': tiempo_terminar_entrenar,
            'menu1': request.form.get('menu1_terminar_entrenar', '').strip(),
            'menu2': request.form.get('menu2_terminar_entrenar', '').strip(),
            'menu3': request.form.get('menu3_terminar_entrenar', '').strip(),
        },
        {
            'tiempo': tiempo_cena,
            'menu1': request.form.get('menu1_cena', '').strip(),
            'menu2': request.form.get('menu2_cena', '').strip(),
            'menu3': request.form.get('menu3_cena', '').strip(),
        }
    ]

    print('Diccionario de manus: ', menus)

    # Validar que todos los menús estén completos
    if any(not menu['tiempo'] or not menu['menu1'] or not menu['menu2'] or not menu['menu3'] for menu in menus):
        flash("Todos los menús deben estar completos.", "danger")
        return redirect(url_for('nutriologo_paciente.index_informacion'))


    # Obtener fecha actual y IDs de día, mes, año
    fecha_actual = datetime.now()
    dia, mes, anio = fecha_actual.day, fecha_actual.month, fecha_actual.year
    meses_espanol = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    mes_espanol = meses_espanol[mes]

    # Verificación de información del paciente
    paciente_info = session.get('paciente_info')
    if not paciente_info:
        flash('No se encontró información del paciente.', 'warning')
        return redirect(url_for('nutriologo_paciente.index_informacion'))
    id_paciente = paciente_info[0]

    # Verificar si ya existe un plan alimenticio para el paciente
    Verificar_existe_un_plan_alimenticio = "SELECT COUNT(*) FROM public.plan_alimenticio WHERE id_paciente_paciente = %s"
    existe_plan = Config.Read(Verificar_existe_un_plan_alimenticio, (id_paciente,))[0][0] > 0

    if existe_plan:
        flash('Solo se permite un plan alimenticio por paciente.', 'danger')
        return redirect(url_for('nutriologo_paciente.index_informacion'))

    # Consulta para obtener IDs de día, mes y año
    consulta_ids = """
        SELECT 
            (SELECT id_dia FROM public.dia WHERE dia = %s) AS id_dia,
            (SELECT id_mes FROM public.mes WHERE mes = %s) AS id_mes,
            (SELECT id_anio FROM public.anio WHERE anio = %s) AS id_anio
    """
    ids_info = Config.Read(consulta_ids, (dia, mes_espanol, anio))
    if not ids_info:
        flash('No se pudo obtener los IDs de día, mes o año.', 'warning')
        return redirect(url_for('nutriologo_paciente.index_informacion'))

    id_dia, id_mes, id_anio = ids_info[0]

    # Registrar el nuevo plan alimenticio en la base de datos
    try:

        Registrar_nuevo_plan_alimenticio = """
        INSERT INTO public.plan_alimenticio (
            alimento_permitido,
            comidas_evitar,
            bebidas_permitidas,
            tips_alimentacion,
            suplementos,
            id_paciente_paciente,
            id_dia_id_dia,
            id_mes_dia_mes,
            id_anio_id_anio
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        # Ejecutar consulta con control de valores nulos en campos opcionales
        Config.CUD(
            Registrar_nuevo_plan_alimenticio, 
            (alimento_permitido, comidas_evitar, bebidas_permitidas, tips_alimentacion, suplementos, id_paciente, id_dia, id_mes, id_anio)
        )

        # Verificar si ya existe un plan alimenticio para el paciente
        Verificar_existe_un_plan_alimenticio = """
            SELECT id_plan_alimenticio 
            FROM public.plan_alimenticio 
            WHERE id_paciente_paciente = %s
        """
        # Ejecutar la consulta y obtener el resultado
        Registro_id_plan_alimenticio = Config.Read(Verificar_existe_un_plan_alimenticio, (id_paciente,))

        # Comprobar si se encontró un plan alimenticio
        if Registro_id_plan_alimenticio:
            id_plan_alimenticio = Registro_id_plan_alimenticio[0][0]  # Asumimos que id_plan_alimenticio es la primera columna
            print(f'ID del Plan Alimenticio: {id_plan_alimenticio}')  # Depuración
        else:
            flash('No se encontró ningún plan alimenticio para el paciente.', 'warning')  # Mostrar mensaje de advertencia
            print('No se encontró ningún plan alimenticio para el paciente.')  # Depuración
            return redirect(url_for('nutriologo_paciente.index_informacion'))  # Redirigir a la página de información del paciente

        # Lista para almacenar los datos de inserción
        Guardar_diccionario_de_menus = []

        for menu in menus:
            # Extraer los datos necesarios
            tiempo_de_comida = menu['tiempo']
            menu1 = menu['menu1']
            menu2 = menu['menu2']
            menu3 = menu['menu3']

            # Agregar los valores a la lista
            Guardar_diccionario_de_menus.append((tiempo_de_comida, menu1, menu2, menu3, id_plan_alimenticio))

        # Consulta de inserción masiva
        Crear_nueva_semana_plan_comida = """
            INSERT INTO public.semana_plan_comida (
                tiempos_de_comida,
                menu_uno_lunes_viernes,
                menu_dos_martes_jueves,
                menu_tres_miercoles_sabado,
                id_plan_alimenticio_plan_alimenticio
            ) VALUES (%s, %s, %s, %s, %s);
        """

        # Ejecutar la consulta para insertar todos los registros
        Config.CUD(
            Crear_nueva_semana_plan_comida,
            Guardar_diccionario_de_menus,
            is_bulk=True  # Asegúrate de que tu función CUD soporte inserciones masivas
        )
        
        flash('Registro ingresado exitosamente.', 'success')
    except Exception as e:
        flash(f'Ocurrió un error al registrar el plan: {str(e)}', 'danger')
        print(f'Error al ejecutar la consulta: {e}')  # Debug para error en consola

    # Redirigir a la página de información del paciente
    return redirect(url_for('nutriologo_paciente.index_informacion'))

@bp.route('/actualizar_plan', methods=['POST'])
def actualizar_plan():

    # Obtener los datos del formulario con validación para campos requeridos
    alimento_permitido = request.form.get('low_calorie_foods', '').strip()
    comidas_evitar = request.form.get('avoid_foods', '').strip()
    bebidas_permitidas = request.form.get('allowed_drinks', '').strip()
    tips_alimentacion = request.form.get('nutrition_tips', '').strip() or "sin tips alimenticios"  # Usar "sin tips" si está vacío
    suplementos = request.form.get('supplement_details', '').strip() or "sin suplementos"  # Usar "sin suplementos" si está vacío
        # Validar la longitud máxima de los campos
    max_length = 1000
    if (
        len(alimento_permitido) > max_length or
        len(comidas_evitar) > max_length or
        len(bebidas_permitidas) > max_length or
        len(tips_alimentacion) > max_length or
        len(suplementos) > max_length
    ):
        flash('Cada campo debe contener un máximo de 1000 caracteres.', 'warning')
        return redirect(url_for('nutriologo_paciente.index_informacion'))

    # Validar id_plan
    id_plan_alimenticio = request.form.get('plan_id', '').strip()
    if not id_plan_alimenticio or not id_plan_alimenticio.isdigit() or int(id_plan_alimenticio) <= 0:
        flash('El ID del plan no puede estar vacío y debe ser un entero positivo.', 'warning')
        return redirect(url_for('nutriologo_paciente.index_informacion'))
    
    # Validar que id_plan no esté vacío y sea un número entero
    if id_plan_alimenticio and id_plan_alimenticio.isdigit():  # Verifica que no esté vacío y que contenga solo dígitos
        id_plan_alimenticio = int(id_plan_alimenticio)  # Convertir a entero
    else:
        # Manejar el caso en que id_plan no sea válido
        flash("El ID del plan debe ser un número entero válido.", "warning")
        return redirect(url_for('nutriologo_paciente.index_informacion'))


    id_tiempos_comida = request.form.getlist('plan_semanal_comida_id[]')

    # Validar campos obligatorios
    if not alimento_permitido or not comidas_evitar or not bebidas_permitidas or len(id_tiempos_comida) < 5:
        flash('Por favor, complete todos los campos obligatorios.', 'warning')
        return redirect(url_for('nutriologo_paciente.index_informacion'))
    
        # Asignar los tiempos de comida
    id_tiempo_desayuno = id_tiempos_comida[0]
    id_tiempo_almuerzo = id_tiempos_comida[1]
    id_tiempo_durante_entrenamiento = id_tiempos_comida[2]
    id_tiempo_terminar_entrenar = id_tiempos_comida[3]
    id_tiempo_cena = id_tiempos_comida[4]

    # Menús para cada tiempo de comida
    menus_actualizar = [
        {
            'id_tiempo': id_tiempo_desayuno,
            'menu1': request.form.get('menu1_desayuno', '').strip(),
            'menu2': request.form.get('menu2_desayuno', '').strip(),
            'menu3': request.form.get('menu3_desayuno', '').strip(),
        },
        {
            'id_tiempo': id_tiempo_almuerzo,
            'menu1': request.form.get('menu1_almuerzo', '').strip(),
            'menu2': request.form.get('menu2_almuerzo', '').strip(),
            'menu3': request.form.get('menu3_almuerzo', '').strip(),
        },
        {
            'id_tiempo': id_tiempo_durante_entrenamiento,
            'menu1': request.form.get('menu1_durante_entrenamiento', '').strip(),
            'menu2': request.form.get('menu2_durante_entrenamiento', '').strip(),
            'menu3': request.form.get('menu3_durante_entrenamiento', '').strip(),
        },
        {
            'id_tiempo': id_tiempo_terminar_entrenar,
            'menu1': request.form.get('menu1_terminar_entrenar', '').strip(),
            'menu2': request.form.get('menu2_terminar_entrenar', '').strip(),
            'menu3': request.form.get('menu3_terminar_entrenar', '').strip(),
        },
        {
            'id_tiempo': id_tiempo_cena,
            'menu1': request.form.get('menu1_cena', '').strip(),
            'menu2': request.form.get('menu2_cena', '').strip(),
            'menu3': request.form.get('menu3_cena', '').strip(),
        }
    ]
    # Imprimir en consola
    print("identificador del plan", id_plan_alimenticio)
    print("Alimento permitido:", alimento_permitido)
    print("Comidas a evitar:", comidas_evitar)
    print("Bebidas permitidas:", bebidas_permitidas)
    print("Tips de alimentación:", tips_alimentacion)
    print("Suplementos:", suplementos)

    print('Diccionario de manus: ', menus_actualizar)

    # Validar que todos los menús estén completos
    if any(not menu['id_tiempo'] or not menu['menu1'] or not menu['menu2'] or not menu['menu3'] for menu in menus_actualizar):
        flash("Todos los menús deben estar completos.", "danger")
        return redirect(url_for('nutriologo_paciente.index_informacion'))
    
    # Obtener fecha actual y IDs de día, mes, año
    fecha_actual = datetime.now()
    dia, mes, anio = fecha_actual.day, fecha_actual.month, fecha_actual.year
    meses_espanol = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    mes_espanol = meses_espanol[mes]

    # Consulta para obtener IDs de día, mes y año
    consulta_ids = """
        SELECT 
            (SELECT id_dia FROM public.dia WHERE dia = %s) AS id_dia,
            (SELECT id_mes FROM public.mes WHERE mes = %s) AS id_mes,
            (SELECT id_anio FROM public.anio WHERE anio = %s) AS id_anio
    """
    ids_info = Config.Read(consulta_ids, (dia, mes_espanol, anio))
    if not ids_info:
        flash('No se pudo obtener los IDs de día, mes o año.', 'warning')
        return redirect(url_for('nutriologo_paciente.index_informacion'))

    id_dia, id_mes, id_anio = ids_info[0]

        # Definir los parámetros para la actualización
    params = (
        alimento_permitido,  # %s
        comidas_evitar,      # %s
        bebidas_permitidas,  # %s
        tips_alimentacion,   # %s
        suplementos,         # %s
        id_dia,      # %s
        id_mes,     # %s
        id_anio,    # %s
        id_plan_alimenticio  # %s (esto es el ID que quieres actualizar)
    )

    try:
        Actualizar_plan_alimenticio = """
        UPDATE public.plan_alimenticio
        SET
            alimento_permitido = %s,
            comidas_evitar = %s,
            bebidas_permitidas = %s,
            tips_alimentacion = %s,
            suplementos = %s,
            id_dia_id_dia = %s,
            id_mes_dia_mes = %s,
            id_anio_id_anio = %s
        WHERE
            id_plan_alimenticio = %s;
        """
        # Ejecutar la consulta de actualización
        Config.CUD(Actualizar_plan_alimenticio, params)

        # Lista para almacenar los datos de inserción
        Guardar_diccionario_de_menus = []

        for menu in menus_actualizar:
            # Extraer los datos necesarios
            id_tiempo_de_comida = menu['id_tiempo']
            menu1 = menu['menu1']
            menu2 = menu['menu2']
            menu3 = menu['menu3']

            # Agregar los valores a la lista
            Guardar_diccionario_de_menus.append((menu1, menu2, menu3, id_tiempo_de_comida))

        # Consulta de inserción masiva
        Actualizar_semana_plan_comida = """
            UPDATE public.semana_plan_comida
            SET
                menu_uno_lunes_viernes = %s,
                menu_dos_martes_jueves = %s,
                menu_tres_miercoles_sabado = %s
            WHERE
                id_comida = %s;
        """

        # Ejecutar la consulta para insertar todos los registros
        Config.CUD(
            Actualizar_semana_plan_comida,
            Guardar_diccionario_de_menus, 
            is_bulk=True  # Asegúrate de que tu función CUD soporte actualizaciones masivas
        )

        print("Actualización exitosa del plan alimenticio.")
        flash("Plan alimenticio actualizado correctamente.", "success")  # Mensaje de éxito
    except Exception as e:
        # Captura cualquier excepción y muestra un mensaje de error
        print(f"Error durante la actualización del plan alimenticio: {e}")
        flash("Error durante la actualización del plan alimenticio.", "error")  # Mensaje de error
        return redirect(url_for('nutriologo_paciente.index_informacion'))


    return redirect(url_for('nutriologo_paciente.index_informacion'))

def obtener_datos_paciente(id_paciente):
    """Función para obtener los datos del paciente, su progreso y su plan alimenticio."""
    
    # Consulta para obtener el progreso más reciente del paciente
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
            a.anio DESC, m.mes DESC, d.dia DESC
        LIMIT 1;
    """

    # Consulta para obtener el plan alimenticio del paciente
    consulta_su_plan_alimentcio_del_paciente = """ 
        SELECT 
            pa.id_plan_alimenticio,
            pa.alimento_permitido,
            pa.comidas_evitar,
            pa.bebidas_permitidas,
            pa.tips_alimentacion,
            pa.suplementos,
            pa.id_paciente_paciente,
            d.dia,
            m.mes,
            a.anio
        FROM 
            public.plan_alimenticio pa
        INNER JOIN 
            public.dia d ON pa.id_dia_id_dia = d.id_dia
        INNER JOIN 
            public.mes m ON pa.id_mes_dia_mes = m.id_mes
        INNER JOIN 
            public.anio a ON pa.id_anio_id_anio = a.id_anio
        WHERE 
            pa.id_paciente_paciente = %s
        ORDER BY 
            a.anio DESC, m.mes DESC, d.dia DESC;
    """

    # Ejecutar consultas
    registro_progreso = Config.Read(Consultar_el_progreso_mas_reciente, (id_paciente,))
    registro_plan_alimenticio = Config.Read(consulta_su_plan_alimentcio_del_paciente, (id_paciente,))

    # Asegurarse de que la consulta devolvió resultados para el plan alimenticio
    if registro_plan_alimenticio:
        # Extraer el primer dato de la primera fila
        id_plan_alimenticio = registro_plan_alimenticio[0][0]
        print("ID del plan alimenticio:", id_plan_alimenticio)

        # Consulta para obtener comidas por semana usando el id del plan alimenticio
        Consultar_comidas_por_semana_paciente = """
            SELECT 
                id_comida, 
                tiempos_de_comida, 
                menu_uno_lunes_viernes, 
                menu_dos_martes_jueves, 
                menu_tres_miercoles_sabado
            FROM 
                public.semana_plan_comida
            WHERE 
                id_plan_alimenticio_plan_alimenticio = %s
            LIMIT 5;
        """
    # Retorna los datos del progreso, el plan alimenticio y el diccionario de comidas
    return registro_progreso, registro_plan_alimenticio

def obtener_plan_comidas_semanal_paciente(id_plan_alimenticio):
    Consultar_comidas_por_semana_paciente = """
    SELECT 
        id_comida, 
        menu_uno_lunes_viernes, 
        menu_dos_martes_jueves, 
        menu_tres_miercoles_sabado
    FROM 
        public.semana_plan_comida
    WHERE 
        id_plan_alimenticio_plan_alimenticio = %s
    LIMIT 5;
    """
    
    try:
        # Ejecuta la consulta y obtiene los registros
        registro_comidas_por_semana_paciente = Config.Read(Consultar_comidas_por_semana_paciente, (id_plan_alimenticio,))
        
        # Si no hay registros, se retorna un dict con lista vacía
        if not registro_comidas_por_semana_paciente:
            return {"comidas": []}

        # Crear el diccionario de comidas
        comidas_dict = {
            "comidas": [
                {
                    "id_comida": row[0],
                    "menu_uno_lunes_viernes": row[1],
                    "menu_dos_martes_jueves": row[2],
                    "menu_tres_miercoles_sabado": row[3],
                }
                for row in registro_comidas_por_semana_paciente
            ]
        }
        return comidas_dict

    except Exception as e:
        print(f"Error al obtener el plan de comidas: {e}")
        return {"comidas": []}  # Retorna un dict vacío si ocurre un error




