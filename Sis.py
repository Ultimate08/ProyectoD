import threading
import sqlite3
import random
import MWf

bd = sqlite3.connect('/home/eduardo/base.sqlite')
cur = bd.cursor()
idP = 1
idC = 1

if __name__ == "__main__":
    # Configuración de los servidores en cada máquina virtual
    hosts = [
        "192.168.153.128",
        "192.168.153.129",
        "192.168.153.130",
        "192.168.153.131"
    ]
    port = 12345  # Puerto para la comunicación entre las máquinas

    maestro = 0 # Bandera que indica que nodo es el maestro

    espera = True # Bandera que espera respuesta

    
    cur.execute('DROP TABLE IF EXISTS PRODUCTO')
    cur.execute('DROP TABLE IF EXISTS CLIENTE')
    cur.execute('DROP TABLE IF EXISTS INVENTARIO')
    # Creacion de tablas
    cur.execute('CREATE TABLE PRODUCTO (idProducto INTEGER, nombre TEXT, total INTEGER)')
    cur.execute('CREATE TABLE CLIENTE (idCliente INTEGER, nombre TEXT, apPaterno TEXT, apMaterno TEXT)')
    cur.execute('CREATE TABLE INVENTARIO (idSucursal, producto INTEGER, cantidad INTEGER)')

    #cur.execute('INSERT INTO PRODUCTOS (idProducto, nombre) VALUES (?, ?)', ('My Way', 15))
    cur.execute('INSERT INTO PRODUCTO (idProducto, nombre, total) VALUES (?, ?, ?)',(idP,'Zapatos', 20))
    idP += 1
    cur.execute('INSERT INTO PRODUCTO (idProducto, nombre, total) VALUES (?, ?, ?)',(idP,'Gorra', 16))
    idP += 1
    cur.execute('INSERT INTO PRODUCTO (idProducto, nombre, total) VALUES (?, ?, ?)',(idP,'Hoodie', 12))
    idP += 1
    cur.execute('INSERT INTO CLIENTE (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,'Brayan','Ambriz','Zuloaga'))
    idC += 1
    cur.execute('INSERT INTO CLIENTE (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,'Eduardo','Fajardo','Tellez'))
    idC += 1
    cur.execute('INSERT INTO CLIENTE (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,'Marcos','Vega','Alvarez'))
    idC += 1

    i = 1
    j = 1
    while i <= len(hosts):
        j = 1
        while j < idP:
            cur.execute('SELECT total FROM PRODUCTO WHERE idProducto = ?',(j, ))
            r = cur.fetchone()
            t = r[0]
            t /= len(hosts)
            cur.execute('INSERT INTO INVENTARIO (idSucursal, producto, cantidad) VALUES (?,?,?)',(i,j,t))
            j += 1
        i += 1
    
    
    bd.commit()
    #conn.close()
    
    # Iniciar los servidores en cada máquina virtual
    for host in hosts:
        server_thread = threading.Thread(target=MWf.servidor, args=(host, port))
        server_thread.start()
    
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
                cur.execute('INSERT INTO CLIENTE (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,n,p,m))
                idC += 1
                bd.commit()
                print("Se agrego el producto ",n," "," ",p," ",m," correctamente")
                #for host in hosts:
                #    mensaje(host,port,"cliente")
                #    mensaje(host,port,nom)
                #    mensaje(host,port,apPat)
                #    mensaje(host,port,apMat)
                
                #espera = True
            elif choice == '3':
               print("")
            elif choice == '4':
                n = input("\nCuál es el nombre del nuevo articulo?: ")
                m = input("\nCuál es la cantidad total del producto??: ")
                cur.execute('INSERT INTO PRODUCTO (idProducto, nombre, total) VALUES (?,?,?)',(id,n,m))
                idP += 1
                bd.commit()
                print("Se agrego el producto ",n," correctamente.")
            elif choice == '5':
                cur.execute('SELECT * FROM INVENTARIO')
                print("(idSucursal, producto, cantidad)")
                for fila in cur:
                    print(fila)
        except ValueError:
            print("Entrada inválida. Ingrese un número válido o '0' para salir.")
