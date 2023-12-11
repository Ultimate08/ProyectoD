import socket
import threading
import sqlite3
import random
import MWf

bd = sqlite3.connect('/home/eduardo/base.sqlite')
cur = bd.cursor()

if __name__ == "__main__":
    # Configuración de los servidores en cada máquina virtual
    hosts = [
        "192.168.153.128",
        "192.168.153.129",
        "192.168.153.130",
        "192.168.153.131"
    ]
    port = [      # Puerto para la comunicación entre las máquinas
        1111,
        2222,
        3333,
        4444
    ]
    
    names = [    # Identificadores de las máquinas
    "56 4d b8 d4 59 5c 11 53-09 55 ae 8a 8f ff 51 50",
    "56 4d dc 63 62 9c cb 1c-13 45 ad 0f 02 0f df 22",
    "56 4d 94 6e e2 81 de 60-8e eb 92 b6 22 ca 2c 9a",
    "56 4d a3 80 4a 63 88 e9-63 94 0e eb 5e af 4c 5c"
    ]

    # Iniciar los servidores en cada máquina virtual
    uuid = MWf.obtener_uuid()
    if (uuid == names[0]):
        vm1 = threading.Thread(target=MWf.servidor, args=(hosts[0], port[0]))
        vm1.start()
    elif (uuid == names[1]):
        vm2 = threading.Thread(target=MWf.servidor, args=(hosts[1], port[1]))
        vm2.start()
    elif (uuid == names[2]):
        vm3 = threading.Thread(target=MWf.servidor, args=(hosts[2], port[2]))
        vm3.start()
    elif (uuid == names[3]):
        vm4 = threading.Thread(target=MWf.servidor, args=(hosts[3], port[3]))
        vm4.start()
    
    while True:
        # Menu de seleccion
        print("\nBienvenido al sistema de inventarios, que deseas hacer?:")
        print("\n1. Consultar clientes")
        print("\n2. Agregar nuevo cliente")
        print("\n3. Comprar articulo")
        print("\n4. Agregar articulo\n")

        choice = input("Ingrese el número de opción correspondiente o '0' para salir: ")
        if choice == '0':
            break
        try:
            if choice == '1':
                cur.execute('SELECT * FROM CLIENTE')
                print("(idCliente, nombre, apPaterno, apMaterno)")
                for fila in cur:
                    print(fila)
            elif choice == '2':
                #bd.execute('BEGIN EXCLUSIVE TRANSACTION')
                n = input("\nCuál es el nombre del cliente?: ")
                p = input("\nCuál es el apellido paterno del cliente?: ")
                m = input("\nCuál es el apellido materno del cliente?: ")
                msj = "cliente "+n+" "+p+" "+m
                MWf.mensaje(hosts[0],port[0],msj)
                MWf.mensaje(hosts[1],port[1],msj)
                MWf.mensaje(hosts[2],port[2],msj)
                MWf.mensaje(hosts[3],port[3],msj)
        
            elif choice == '3':
               print("")
            elif choice == '4':
                #bd.execute('BEGIN EXCLUSIVE TRANSACTION')
                a = input("\nCuál es el nombre del nuevo articulo?: ")
                p = input("\nCuál es la cantidad total del articulo?: ")
                msj = "articulo "+a+" "+p
                MWf.mensaje(hosts[0],port[0],msj)
                MWf.mensaje(hosts[1],port[1],msj)
                MWf.mensaje(hosts[2],port[2],msj)
                MWf.mensaje(hosts[3],port[3],msj)
                
            elif choice == '5':
                cur.execute('SELECT * FROM INVENTARIO')
                print("(idSucursal, producto, cantidad)")
                for fila in cur:
                    print(fila)
            elif choice == '6':
                cur.execute('SELECT * FROM PRODUCTO')
                print("(idProducto, nombre, total)")
                for fila in cur:
                    print(fila)
        except ValueError:
            print("Entrada inválida. Ingrese un número válido o '0' para salir.")
