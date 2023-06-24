import colorama
import socket
from colorama import Fore

colorama.init(autoreset=True)

HOST = 'localhost'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        print(Fore.BLUE +"Transacciones de pago examen\n\n")
        print(Fore.BLUE +'Elija una opción:\n')
        print(Fore.BLUE +'1. Metodo Consulta')
        print(Fore.BLUE +'2. Metodo de pago')
        print(Fore.BLUE +'3. Revertir pago')
        print(Fore.BLUE +'4. Salir')

        opcion = input('Opción: ')

        if opcion == '1':
            codigo_cliente = input("Ingrese el codigo del cliente y codigo de documento: ")

            mensaje = f'LEER {codigo_cliente}\n'
            s.sendall(mensaje.encode())

            data = s.recv(1024)
            data = data.decode().split('/')
            print(Fore.GREEN + 'Respuesta: ' + (data[0].strip()))

            print('\n')

        elif opcion == '2':
            codigo_cliente = input('Ingrese el codigo del cliente y numero de documento: ')

            mensaje = f'METODOPAGO {codigo_cliente}\n'
            s.sendall(mensaje.encode())
            data = s.recv(1024)
            print(Fore.GREEN + 'Respuesta: ', data.decode())

            print('\n')

        elif opcion == '3':
            codigo_cliente = input('Ingrese el numero de transaccion: ')

            mensaje = f'REVERTIR {codigo_cliente}\n'
            s.sendall(mensaje.encode())
            data = s.recv(1024)

            print(Fore.GREEN + 'Respuesta: ', data.decode())

        elif opcion == '4':
            s.sendall(b'SALIR\n')
            data = s.recv(1024)
            print('Respuesta del servidor:', data.decode())
            break
        else:
            print(Fore.RED +'Opción no válida. Inténtelo de nuevo.')