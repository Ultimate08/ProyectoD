import socket
import threading
import sqlite3
import random
import MWf

ipl = ''
hn = socket.gethostname()
ipl = socket.gethostbyname(hn)

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

    # Iniciar los servidores en cada máquina virtual
    if (ipl == hosts[0]):
        vm1 = threading.Thread(target=servidor, args=(hosts[0], port[0]))
        vm1.start()
    elif (ipl == hosts[1]):
        vm2 = threading.Thread(target=servidor, args=(hosts[1], port[1]))
        vm2.start()
    elif (ipl == hosts[2]):
        vm3 = threading.Thread(target=servidor, args=(hosts[2], port[2]))
        vm3.start()
    elif (ipl == hosts[3]):
        vm4 = threading.Thread(target=servidor, args=(hosts[3], port[3]))
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
                n = input("\nCuál es el nombre del cliente?: ")
                p = input("\nCuál es el apellido paterno del cliente?: ")
                m = input("\nCuál es el apellido materno del cliente?: ")
                MWf.mensaje(hosts[0],port[0],bd)
                MWf.mensaje(hosts[1],port[1],bd)
                MWf.mensaje(hosts[2],port[2],bd)
                MWf.mensaje(hosts[3],port[3],bd)
        
            elif choice == '3':
               print("")
            elif choice == '4':
                a = input("\nCuál es el nombre del nuevo articulo?: ")
                p = input("\nCuál es la cantidad total del producto??: ")
                cur.execute('INSERT INTO PRODUCTO (idProducto, nombre, total) VALUES (?,?,?)',(idP,a,p))
                idP += 1

                x = 0
                n = int(p)
                m = len(hosts)
                t = [n//m]*m
                r = n % m
                for z in range(r):
                    t[z] += 1
                cur.execute('INSERT INTO INVENTARIO (idSucursal, producto, cantidad) VALUES (?,?,?)',(j,idP-1,t[j-1]))
                bd.commit()
                print("Se agrego el producto ",a," correctamente.")
                
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
