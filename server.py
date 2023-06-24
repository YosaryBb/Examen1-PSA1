import socket
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="1234",
    database="db_main"
)

HOST = 'localhost'
PORT = 12345


def leer_registro(id):
    cursor = db.cursor()

    sql = "SELECT CONCAT(CodigoDocumento, Monto) CDM FROM Transacciones WHERE CONCAT(CodigoCliente, CodigoDocumento) = %s"
    val = (id,)

    cursor.execute(sql, val)
    resultado = cursor.fetchone()

    if resultado:
        return resultado
    else:
        return "No se encontró el registro"


def metodo_pago(id):
    cursor = db.cursor()

    sql = "SELECT * FROM Transacciones WHERE CONCAT(CodigoCliente, CodigoDocumento) = %s"
    val = (id,)

    cursor.execute(sql, val)
    resultado = cursor.fetchone()

    if resultado:
        response = change_status(id, 'A')

        code = '00' if response else '01'
        sql = f"SELECT CONCAT('{code}', Transaccion) AS CDM FROM Transacciones WHERE CONCAT(CodigoCliente, " \
              f"CodigoDocumento) = %s"

        cursor.execute(sql, val)
        resultado2 = cursor.fetchone()

        return resultado2
    else:
        return "No se encontró el registro"


def revertir_pago(id):
    cursor = db.cursor()

    sql = "SELECT CONCAT(CodigoCliente, CodigoDocumento) DM FROM Transacciones WHERE Transaccion = %s"
    val = (id,)

    cursor.execute(sql, val)
    resultado = cursor.fetchone()

    if resultado:
        response = change_status(resultado[0], 'P')
        code = '00' if response else '01'

        return code
    else:
        return "No se encontró el registro"


def change_status(id, status):
    cursor = db.cursor()

    sql = f"UPDATE Transacciones SET Estado = '{status}' WHERE CONCAT(CodigoCliente, CodigoDocumento) = %s"
    val = (id,)

    cursor.execute(sql, val)
    db.commit()

    return cursor.rowcount


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('El servidor está listo para recibir conexiones')

    conn, addr = s.accept()

    with conn:
        print('Conexión establecida desde', addr)

        while True:
            data = conn.recv(1024)
            mensaje = data.decode().split()
            comando = mensaje[0]

            if comando == "LEER":
                resultados = leer_registro(mensaje[1])
                if resultados:
                    respuesta = f" /    ".join([str(resultado) for resultado in resultados])
                else:
                    respuesta = "No se encontraron registros"
            elif comando == "METODOPAGO":
                resultados = metodo_pago(mensaje[1])
                if resultados:
                    respuesta = f" /    ".join([str(resultado) for resultado in resultados])
                else:
                    respuesta = "No se encontraron registros"
            elif comando == "REVERTIR":
                resultado = revertir_pago(mensaje[1])
                if resultado:
                    respuesta = f" /    {resultado}"
                else:
                    respuesta = "No se encontraron registros"
            elif comando == "SALIR":
                respuesta = "Saliendo del programa"
                break
            else:
                respuesta = "Comando no válido"
            conn.sendall(respuesta.encode())