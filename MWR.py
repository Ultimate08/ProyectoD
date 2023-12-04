import socket
import threading
import time
import sqlite3
import random

bd = sqlite3.connect('base.sqlite')
cur = bd.cursor()
idP = 1
idC = 1

def cliente(conn, addr):
    print(f'Conectado por {addr}')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        received_message = data.decode()
        if received_message == "cliente":
            n = conn.recv(1024)
            p = conn.recv(1024)
            a = conn.recv(1024)
            cur.execute('INSERT INTO CLIENTES (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,n,p,m))
            idC += 1
            bd.commit()
        print(f'Mensaje recibido de {addr}: {received_message}')
        
        # Almacenar mensaje recibido en un archivo
        with open(f"msgs.txt", "a") as file:
            file.write(f"[Recibido] {time.strftime('%Y-%m-%d %H:%M:%S')} - {received_message}\n")
        
        # Enviar un mensaje de confirmación al cliente
        confirmation_message = "Recibido"
        conn.sendall(confirmation_message.encode())
        print(f'Mensaje de confirmación enviado a {addr}: {confirmation_message}')

    conn.close()

def servidor(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print(f"Servidor escuchando en {host}:{port}")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=cliente, args=(conn, addr))
            client_thread.start()

def mensaje(server_ip, server_port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        mt = f"[{t}] {message}"
        s.sendall(mt.encode())
        print(f"Mensaje enviado a {server_ip}:{server_port}: {mt}")
        
        # Almacenar mensaje enviado en un archivo
        with open(f"msgs.txt", "a") as file:
            file.write(f"[Enviado] {t} - {message}\n")
        
        response = s.recv(1024)
        decoded_response = response.decode()
        print(f"Respuesta del servidor {server_ip}:{server_port}: {decoded_response}")
        
        # Almacenar mensaje de confirmación recibido en un archivo
        with open(f"msgs.txt", "a") as file:
            file.write(f"[Recibido] {time.strftime('%Y-%m-%d %H:%M:%S')} - {decoded_response}\n")

def select_leader(my_id, servers):
    global coordinator
    higher_servers = [server for server in servers if int(server.split('.')[-1]) > int(my_id.split('.')[-1])]
    for higher_server in higher_servers:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((higher_server, port))
                s.sendall("Election".encode())
                response = s.recv(1024).decode()
                if response == "I_am_leader":
                    coordinator = higher_server
                    print(f"{my_id} - Coordinador es {coordinator}")
                    return
            except ConnectionRefusedError:
                pass
    coordinator = my_id
    print(f"{my_id} - Coordinador es {coordinator}")

def llenarDB(server_ip, port, id, n, p, m):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, port))
        s.sendall(id.encode())
        s.sendall(n.encode())
        s.sendall(p.encode())
        s.sendall(m.encode())
        #Agregar los datos a la base de datos
        cur.execute('INSERT INTO CLIENTES (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(id,n,p,m))
        id += 1
        bd.commit()


def mutex():
    print(" ")

def compra():
    print(" ")
    
def n_cliente():
    print(" ")

if __name__ == "__main__":
    # Configuración de los servidores en cada máquina virtual
    hosts = [
        #'localhost'
        '''
        "192.168.153.128",
        "192.168.153.129",
        "192.168.153.130",
        "192.168.153.131"
        '''
    ]

    miDir = "192.168.153.128"

    port = 12345  # Puerto para la comunicación entre las máquinas

    maestro = 0 # Bandera que indica que nodo es el maestro

    espera = True # Bandera que espera respuesta

    
    cur.execute('DROP TABLE IF EXISTS PRODUCTOS')
    cur.execute('DROP TABLE IF EXISTS CLIENTES')
    cur.execute('DROP TABLE IF EXISTS INVENTARIO')
    # Creacion de tablas
    cur.execute('CREATE TABLE PRODUCTOS (idProducto INTEGER, nombre TEXT)')
    cur.execute('CREATE TABLE CLIENTES (idCliente INTEGER, nombre TEXT, apPaterno TEXT, apMaterno TEXT)')
    cur.execute('CREATE TABLE INVENTARIO (idSucursal, producto TEXT, cantidad INTEGER)')

    #cur.execute('INSERT INTO PRODUCTOS (idProducto, nombre) VALUES (?, ?)', ('My Way', 15))
    cur.execute('INSERT INTO PRODUCTOS (idProducto, nombre) VALUES (?, ?)',(idP,'Zapatos'))
    idP += 1
    cur.execute('INSERT INTO PRODUCTOS (idProducto, nombre) VALUES (?, ?)',(idP,'Gorra'))
    idP += 1
    cur.execute('INSERT INTO PRODUCTOS (idProducto, nombre) VALUES (?, ?)',(idP,'Hoodie'))
    idP += 1
    cur.execute('INSERT INTO CLIENTES (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,'Brayan','Ambriz','Zuloaga'))
    idC += 1
    cur.execute('INSERT INTO CLIENTES (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,'Eduardo','Fajardo','Tellez'))
    idC += 1
    cur.execute('INSERT INTO CLIENTES (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,'Marcos','Vega','Alvarez'))
    idC += 1
    bd.commit()
    #conn.close()
    
    # Iniciar los servidores en cada máquina virtual
    for host in hosts:
        server_thread = threading.Thread(target=servidor, args=(host, port))
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
                cur.execute('SELECT * FROM CLIENTES')
                print("(idCliente, nombre, apPaterno, apMaterno)")
                for fila in cur:
                    print(fila)
            elif choice == '2':
                n = input("\nCuál es el nombre del cliente?: ")
                p = input("\nCuál es el apellido paterno del cliente?: ")
                m = input("\nCuál es el apellido materno del cliente?: ")
                print(dir)
                for i in hosts:
                    print(i)
                cur.execute('INSERT INTO CLIENTES (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,n,p,m))
                idC += 1
                bd.commit()

                #Funcion que sirve para enviar 
                '''for host in hosts:
                    mensaje(host,port,"cliente")
                    mensaje(host,port,nom)
                    mensaje(host,port,apPat)
                    mensaje(host,port,apMat)'''
                
                for i in hosts:
                    if miDir != i:
                        llenarDB(i, port, idC, n, p, m)   
                
                espera = True
            elif choice == '3':
                
                espera = True
            elif choice == '4':
                
                espera = True
            elif choice == '5':
                
                espera = True
        except ValueError:
            print("Entrada inválida. Ingrese un número válido o '0' para salir.")

