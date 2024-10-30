import psycopg2
from flask import redirect, session, flash, url_for

HEX_SEC_KEY = "d5fb8c4fa8bd46638dadc4e751e0d68d"

ROLE_CREDENTIALS = {
    'nutriologo': {
        'user': 'nutriologo',
        'password': 'T!6ry@9g#@c1t2b&z#@k'
    },
    'paciente': {
        'user': 'paciente',
        'password': 'Y#8fL*5nV!q0G3z&xT9e'
    },
    'superusuario': {
        'user': 'superusuario',
        'password': 'T6645697#5x1@#b@z48k'
    },
    'visitante': {
        'user': 'visitante',
        'password': 'T!6rF@9gQ#x1V2b&zP8k'
    }
}

def get_credentials(role):
    return ROLE_CREDENTIALS.get(role, ROLE_CREDENTIALS['visitante'])

def CUD(query, params=None, is_bulk=False, max_retries=3):
    print("<-------------------- Conectando... --------------------")
    connection = None
    try:
        role = session.get('rol', 'visitante')
        print(f"Rol en sesión: {role}")
        credentials = get_credentials(role)
        print(f"Usuario en conexión: {credentials['user']}")

        connection = psycopg2.connect(
            dbname="nutriologo_db",
            user=str(credentials['user']),
            password=str(credentials['password']),
            host="localhost",
            port="5432"
        )

        cursor = connection.cursor()
        retries = 0

        while retries < max_retries:
            try:
                # Iniciar la transacción
                cursor.execute("BEGIN;")
                
                if is_bulk and isinstance(params, list):
                    cursor.executemany(query, params)
                else:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)

                # Confirmar cambios
                cursor.execute("COMMIT;")
                print("<-------------------- Conexión exitosa --------------------")
                break  # Salir del bucle si la operación fue exitosa
            
            except (psycopg2.OperationalError, psycopg2.DataError) as err:
                print(f"<-------------------- Error: {err} -------------------->")
                # Revertir los cambios
                cursor.execute("ROLLBACK;")
                retries += 1  # Incrementar el número de reintentos
                if retries >= max_retries:
                    flash(f"Error: {err}", 'permiso_denegado')
                    print("<-------------------- Fallo en los reintentos -------------------->")

    except Exception as ex:
        print(f"<-------------------- Error inesperado: {ex} -------------------->")
    finally:
        if connection:
            cursor.close()  # Cerrar cursor
            connection.close()  # Cerrar conexión
            print("-------------------- Conexión finalizada -------------------->")

def Read(query, params=None):
    print("<-------------------- Conectando... --------------------")
    connection = None
    try:
        role = session.get('rol', 'visitante')
        print(f"Rol en sesión: {role}")
        credentials = get_credentials(role)
        print(f"Usuario en conexión: {credentials['user']}")

        connection = psycopg2.connect(
            dbname="nutriologo_db",
            user=str(credentials['user']),
            password=str(credentials['password']),
            host="localhost",
            port="5432"
        )

        cursor = connection.cursor()
        
        # Ejecutar la consulta
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        rows = cursor.fetchall()
        results = [list(row) for row in rows]
        print("<-------------------- Conexión exitosa --------------------")
        
        if results:
            for result in results:
                print(result)
        else:
            print("No se encontraron resultados.")
        
        print("---------------------------------------->")
        return results

    except Exception as ex:
        print(f"<-------------------- Error inesperado: {ex} -------------------->")
        return []
    finally:
        if connection:
            cursor.close()  # Cerrar cursor
            connection.close()  # Cerrar conexión
            print("-------------------- Conexión finalizada -------------------->")
