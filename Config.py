import psycopg2
from flask import redirect, session, flash, url_for

# Clave de seguridad (aunque no se utiliza en este código, la dejé aquí por si la necesitas)
HEX_SEC_KEY = "d5fb8c4fa8bd46638dadc4e751e0d68d"

# Contraseñas por defecto para cada rol
ROLE_CREDENTIALS = {
    'nutriologo': {
        'user': 'nutriologo',
        'password': 'T!6ry@9g#@c1t2b&z#@k'  # Contraseña segura
    },
    'paciente': {
        'user': 'paciente',
        'password': 'Y#8fL*5nV!q0G3z&xT9e'  # Contraseña segura
    },
    'superusuario': {
        'user': 'superusuario',
        'password': 'T6645697#5x1@#b@z48k'  # Contraseña segura
    },
    'visitante': {
        'user': 'visitante',
        'password': 'T!6rF@9gQ#x1V2b&zP8k'  # Contraseña segura
    }
}

# Método para obtener las credenciales según el rol
def get_credentials(role):
    return ROLE_CREDENTIALS.get(role, ROLE_CREDENTIALS['visitante'])  # Devuelve visitante si el rol no existe

# Método para realizar CUD: CREATE, UPDATE y DELETE
def CUD(query, params=None, is_bulk=False):
    print("<-------------------- Conectando... --------------------")
    connection = None
    try:
        # Obtener el rol de la sesión, o usar 'visitante' si no hay rol
        role = session.get('rol', 'visitante')  # Asignar 'visitante' si no hay rol
        print(f"Rol en sesión: {role}")

        # Obtener credenciales según el rol
        credentials = get_credentials(role)
        print(f"Usuario en conexion: {credentials['user']}")
        print(f"Contraseña en conexion: {credentials['password']}")

        # Conectar a la base de datos usando las credenciales obtenidas
        connection = psycopg2.connect(
            dbname="nutriologo_db",  # Nombre de la base de datos
            user=str(credentials['user']),  # Convertir a string  # Usuario según el rol
            password=str(credentials['password']),  # Convertir a string  # Contraseña según el rol
            host="localhost",  # Cambia esto si tu servidor está en otra dirección
            port="5432"  # Puerto por defecto de PostgreSQL
        )
        print(f"conexion a la debe desde: {connection}")
        cursor = connection.cursor()

        # Comprobar si es una inserción masiva
        if is_bulk and isinstance(params, list):
            cursor.executemany(query, params)  # Ejecutar inserciones masivas
        else:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

        connection.commit()  # Confirmar los cambios en la base de datos
        print("<-------------------- Conexión exitosa --------------------")
    except psycopg2.OperationalError as op_err:
        print(f"<-------------------- Error de operación: {op_err} -------------------->")
    except psycopg2.ProgrammingError as prog_err:
        print(f"<-------------------- Error de programación: {prog_err} -------------------->")
        flash(f"Error: {prog_err}", 'permiso_denegado')
    except psycopg2.DataError as data_err:
        print(f"<-------------------- Error de datos: {data_err} -------------------->")
    except UnicodeDecodeError as decode_err:
        print(f"<-------------------- Error de codificación: {decode_err} -------------------->")
    except Exception as ex:
        print(f"<-------------------- Error inesperado: {ex} -------------------->")
    finally:
        if connection:
            connection.close()
            print("-------------------- Conexión finalizada -------------------->")


def Read(query, params=None):
    print("<-------------------- Conectando... --------------------")
    connection = None
    try:
        # Obtener el rol de la sesión, o usar 'visitante' si no hay rol
        role = session.get('rol', 'visitante')  # Asignar 'visitante' si no hay rol
        print(f"Rol en sesión: {role}")

        # Obtener credenciales según el rol
        credentials = get_credentials(role)
        print(f"Usuario en conexion: {credentials['user']}")
        print(f"Contraseña en conexion: {credentials['password']}")

        # Conectar a la base de datos usando las credenciales obtenidas
        connection = psycopg2.connect(
            dbname="nutriologo_db",  # Nombre de la base de datos
            user = str(credentials['user']),  # Convertir a string  # Usuario según el rol
            password = str(credentials['password']),  # Convertir a string  # Contraseña según el rol
            host="localhost",  # Cambia esto si tu servidor está en otra dirección
            port="5432"  # Puerto por defecto de PostgreSQL
        )
        print(f"conexion a la debe desde: {connection}")
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        results = [list(row) for row in rows]  # Convertir cada fila a una lista
        print("<-------------------- Conexión exitosa --------------------")
        for result in results: # mostrar los resultados
            print(result)
        print("---------------------------------------->")
        return results
    except psycopg2.OperationalError as op_err:
        print(f"<-------------------- Error de operación: {op_err} -------------------->")
    except psycopg2.ProgrammingError as prog_err:
        print(f"<-------------------- Error de programación: {prog_err} -------------------->")
    except psycopg2.DataError as data_err:
        print(f"<-------------------- Error de datos: {data_err} -------------------->")
    except UnicodeDecodeError as decode_err:
        print(f"<-------------------- Error de codificación: {decode_err} -------------------->")
    except Exception as ex:
        print(f"<-------------------- Error inesperado: {ex} -------------------->")
        return None
    finally:
        if connection:
            connection.close()
            print("-------------------- Conexión finalizada -------------------->")
