import socket
import threading
import sqlite3
import time
import MWf

bd = sqlite3.connect('/home/eduardo/base.sqlite', check_same_thread=False)
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
    
    names = [    # Nombres dehost de las máquinas
        "VM1",
        "VM2",
        "VM3",
        "VM4"
    ]

    # Iniciar los servidores en cada máquina virtual
    hn = socket.gethostname()
    if (hn == names[0]):
        vm1 = threading.Thread(target=MWf.servidor, args=(hosts[0], port[0]))
        vm1.start()
    elif (hn == names[1]):
        vm2 = threading.Thread(target=MWf.servidor, args=(hosts[1], port[1]))
        vm2.start()
    elif (hn == names[2]):
        vm3 = threading.Thread(target=MWf.servidor, args=(hosts[2], port[2]))
        vm3.start()
    elif (hn == names[3]):
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
                n = input("\nCuál es el nombre del cliente?: ")
                p = input("\nCuál es el apellido paterno del cliente?: ")
                m = input("\nCuál es el apellido materno del cliente?: ")
                cur.execute('SELECT COUNT(*) FROM CLIENTE')
                id = cur.fetchone()[0]
                id += 1
                ids = str(id)
                msj = "cliente "+ids+" "+n+" "+p+" "+m
                cur.execute('INSERT INTO CLIENTE (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(ids,n,p,m))
                
                if (hn == names[0]):
                    MWf.mensaje(hosts[1],port[1],msj)
                    MWf.mensaje(hosts[2],port[2],msj)
                    MWf.mensaje(hosts[3],port[3],msj)
                elif (hn == names[1]):
                    MWf.mensaje(hosts[0],port[0],msj)
                    MWf.mensaje(hosts[2],port[2],msj)
                    MWf.mensaje(hosts[3],port[3],msj)
                elif (hn == names[2]):
                    MWf.mensaje(hosts[0],port[0],msj)
                    MWf.mensaje(hosts[1],port[1],msj)
                    MWf.mensaje(hosts[3],port[3],msj)
                elif (hn == names[3]):
                    MWf.mensaje(hosts[0],port[0],msj)
                    MWf.mensaje(hosts[1],port[1],msj)
                    MWf.mensaje(hosts[2],port[2],msj)

                #i = 0
                #while (i < len(hosts)):
                    #try:
                        #bd.execute('BEGIN EXCLUSIVE TRANSACTION')
                        #MWf.mensaje(hosts[i],port[i],msj)
                        #i += 1
                        #bd.commit()
                        #time.sleep(5) 
                    #except Exception as e:
                        #print(f"Error en la transacción: {e}")
                        #bd.rollback()
        
            elif choice == '3':
               print("")
            elif choice == '4':
                a = input("\nCuál es el nombre del nuevo articulo?: ")
                p = input("\nCuál es la cantidad total del articulo?: ")
                cur.execute('SELECT COUNT(*) FROM PRODUCTO')
                id = cur.fetchone()[0]
                id += 1
                ids = str(id)
                msj = "articulo "+ids" "+a+" "+p
                if (hn == names[0]):
                    MWf.mensaje(hosts[1],port[1],msj)
                    MWf.mensaje(hosts[2],port[2],msj)
                    MWf.mensaje(hosts[3],port[3],msj)
                elif (hn == names[1]):
                    MWf.mensaje(hosts[0],port[0],msj)
                    MWf.mensaje(hosts[2],port[2],msj)
                    MWf.mensaje(hosts[3],port[3],msj)
                elif (hn == names[2]):
                    MWf.mensaje(hosts[0],port[0],msj)
                    MWf.mensaje(hosts[1],port[1],msj)
                    MWf.mensaje(hosts[3],port[3],msj)
                elif (hn == names[3]):
                    MWf.mensaje(hosts[0],port[0],msj)
                    MWf.mensaje(hosts[1],port[1],msj)
                    MWf.mensaje(hosts[2],port[2],msj)
                
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
