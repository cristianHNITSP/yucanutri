import psycopg2
from flask import session

# Clave de seguridad (aunque no se utiliza en este código, la dejé aquí por si la necesitas)
HEX_SEC_KEY = "d5fb8c4fa8bd46638dadc4e751e0d68d"

# Método para realizar CUD: CREATE, UPDATE y DELETE
def CUD(query, params=None):
    print("<-------------------- Conectando... --------------------")
    connection = None
    try:
        # Imprimir los valores de la sesión
        print(f"Correo en sesión: {session.get('correo')}")
        print(f"Contraseña en sesión: {session.get('contraseña')}")

        # Conectar a la base de datos usando las credenciales de la sesión
        connection = psycopg2.connect(
            dbname="nutritionist_db",  # Nombre de la base de datos
            user=str(session['correo']),  # Convertir a string
            password=str(session['contraseña']),  # Convertir a string
            host="localhost",  # Cambia esto si tu servidor está en otra dirección
            port="5432"  # Puerto por defecto de PostgreSQL
        )
        cursor = connection.cursor()
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
        # Imprimir los valores de la sesión
        print(f"Correo en sesión: {session.get('correo')}")
        print(f"Contraseña en sesión: {session.get('contraseña')}")

        connection = psycopg2.connect(
            dbname="nutritionist_db",  # Nombre de la base de datos
            user=str(session['correo']),  # Convertir a string
            password=str(session['contraseña']),  # Convertir a string
            host="localhost",  # Cambia esto si tu servidor está en otra dirección
            port="5432"  # Puerto por defecto de PostgreSQL
        )
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        results = [list(row) for row in rows]  # Convertir cada fila a una lista
        print("<-------------------- Conexión exitosa --------------------")
        for result in results:
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
