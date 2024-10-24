from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import Config as Config
from werkzeug.security import generate_password_hash


bp = Blueprint('nutriologo_paciente', __name__, url_prefix='/nutriologo_paciente')


@bp.route('/index_informacion')
def index_informacion():
    # Verificar si el rol está en la sesión
    rol = session.get('rol')
    if not rol:
        flash('Debes iniciar sesión para acceder a esta página.', 'error')
        return redirect(url_for('auth.inicio_sesion'))  # Redirige a la página de inicio de sesión

    # Paso 1: Obtener el ID del paciente desde la sesión
    paciente_info = session.get('paciente_info')  # Suponiendo que paciente_info ya está guardado
    if not paciente_info:
        print("Error: No se encontró información del paciente en la sesión.")
        flash('No se encontró información del paciente.', 'error')
        return render_template("index_informacion.html")

    id_paciente = paciente_info[0]  # Extraemos el ID del paciente (primer elemento)
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
        registro_progreso = Config.Read(Consultar_el_progreso_mas_reciente, (id_paciente,))  # Llamamos a Config.Read pasándole el ID del paciente
        print(f"Consulta ejecutada con éxito para el paciente ID: {id_paciente}")

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
            print("Advertencia: No se encontraron registros de progreso para este paciente.")
            flash('No se encontraron registros de progreso para este paciente.', 'warning')
            return render_template("index_informacion.html", paciente_info=paciente_info)

    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        flash('Ha ocurrido un error al recuperar la información del progreso. Por favor, inténtalo de nuevo.', 'error')
        return render_template("index_informacion.html", paciente_info=paciente_info)

@bp.route('/crear_nuevo_progreso')
def crear_nuevo_progreso():
    return render_template