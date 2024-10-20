import psycopg2

# Clave de seguridad (aunque no se utiliza en este código, la dejé aquí por si la necesitas)
HEX_SEC_KEY = "d5fb8c4fa8bd46638dadc4e751e0d68d"

# Método para realizar CUD: CREATE, UPDATE y DELETE
def CUD(query, params=None):
    print("<-------------------- Conectando... --------------------")
    try:
        # Conectar a la base de datos
        connection = psycopg2.connect(
            dbname="nutritionist_db",  # Nombre de la base de datos
            user="postgres",  # Tu usuario de PostgreSQL
            password="admin123",  # Tu contraseña
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
    except Exception as ex:
        print(f"<-------------------- Error: {ex} -------------------->")
    finally:
        if connection:
            connection.close()
            print("-------------------- Conexión finalizada -------------------->")


def Read(query, params=None):
    print("<-------------------- Conectando... --------------------")
    connection = None
    try:
        connection = psycopg2.connect(
            dbname="nutritionist_db",  # Nombre de la base de datos
            user="postgres",  # Tu usuario de PostgreSQL
            password="admin123",  # Tu contraseña
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
    except Exception as ex:
        print(f"<-------------------- Error: {ex} -------------------->")
        return None
    finally:
        if connection:
            connection.close()
            print("-------------------- Conexión finalizada -------------------->")
