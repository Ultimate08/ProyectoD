import socket
import threading
import time
import sqlite3
import random

def cliente(conn, addr):
    print(f'Conectado por {addr}')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        received_message = data.decode()
        print(f'Mensaje recibido de {addr}: {received_message}')
        
        # Almacenar mensaje recibido en un archivo
        with open(f"/home/eduardo/msgs.txt", "a") as file:
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
        with open(f"/home/eduardo/msgs.txt", "a") as file:
            file.write(f"[Enviado] {t} - {message}\n")
        
        response = s.recv(1024)
        decoded_response = response.decode()
        print(f"Respuesta del servidor {server_ip}:{server_port}: {decoded_response}")
        
        # Almacenar mensaje de confirmación recibido en un archivo
        with open(f"/home/eduardo/msgs.txt", "a") as file:
            file.write(f"[Recibido] {time.strftime('%Y-%m-%d %H:%M:%S')} - {decoded_response}\n")

def maestro(h, m):
    try:
        choice_idx = m - 1
        if 0 <= choice_idx < len(h):
            server_ip = h[choice_idx]
            message = ""
            mensaje(server_ip, port, message)
    except ValueError:
        print("Sin conexión")

def mutex():
    print(" ")

def compra():
    print(" ")
    
def n_cliente():
    print(" ")

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

    espera = False # Bandera que espera respuesta

    bd = sqlite3.connect('/home/eduardo/base.sqlite')
    cur = bd.cursor()
    idP = 1
    idC = 1
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
            if choice == 1:
                cur.execute('SELECT * FROM CLIENTES')
                for fila in cur:
                    print(fila)
            elif choice == 2:

                espera = True
            elif choice == 3:
                
                espera = True
            elif choice == 4:
                
                espera = True
            elif choice == 5:
                
                espera = True
            else:
                print("Opción inválida. Intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingrese un número válido o '0' para salir.")

        while seguir:
            # Espera por datos
            peticion = socket_cliente.recv(1024)
         
            # Si recibimos cero bytes, es que el cliente ha cerrado el socket
            if not peticion:
                espera = False

            # Contestacion a maestro"
            if ("maestro"==peticion.decode()):
                print (str(datos_cliente)+ " envia hola: contesto")
                socket_cliente.send("pues hola".encode())
             
            # Contestacion y cierre a "adios"
            if ("adios"==peticion.decode()):
                print (str(datos_cliente)+ " envia adios: contesto y desconecto")
                socket_cliente.send("pues adios".encode())
                socket_cliente.close()
                print ("desconectado "+str(datos_cliente))
                espera = False

