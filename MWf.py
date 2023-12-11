import socket
import threading
import sqlite3
import time
import subprocess

bd = sqlite3.connect('/home/eduardo/base.sqlite')
cur = bd.cursor()
idP = 1
idC = 1

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

names = [
    "56 4d b8 d4 59 5c 11 53-09 55 ae 8a 8f ff 51 50",
    "56 4d dc 63 62 9c cb 1c-13 45 ad 0f 02 0f df 22",
    "56 4d 94 6e e2 81 de 60-8e eb 92 b6 22 ca 2c 9a",
    "56 4d a3 80 4a 63 88 e9-63 94 0e eb 5e af 4c 5c"
]

maestro = 0 # Bandera que indica que nodo es el maestro

def cliente(conn, addr):
    global idC
    global idP
    print(f'Conectado por {addr}')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        received_message = data.decode()
        str = received_message.split(sep=' ')
        if str[1] == 'cliente':
            n = str[2]
            p = str[3]
            m = str[4]
            try:
                bd.execute('BEGIN EXCLUSIVE TRANSACTION')
                cur.execute('INSERT INTO CLIENTE (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,n,p,m))
                idC += 1
                bd.commit()
                print("Se agrego el cliente ",n," ",p," ",m," correctamente")
            except Exception as e:
                print(f"Error en la transacción: {e}")
                bd.rollback()
            
        elif str[1] == 'articulo':
            uuid = obtener_uuid()
            w = -1
            if (uuid == names[0]):
                w = 1
            elif (uuid == names[1]):
                w = 2
            elif (uuid == names[2]):
                w = 3
            elif (uuid == names[3]):
                w = 4
            a = str[2]
            b = str[3]
            bd.execute('BEGIN EXCLUSIVE TRANSACTION')
            cur.execute('INSERT INTO PRODUCTO (idProducto, nombre, total) VALUES (?,?,?)',(idP,a,b))
            idP += 1
            n = int(p)
            m = len(hosts)
            t = [n//m]*m
            r = n % m
            for z in range(r):
                t[z] += 1
            cur.execute('INSERT INTO INVENTARIO (idSucursal, producto, cantidad) VALUES (?,?,?)',(w,idP-1,t[w-1]))
            bd.commit()
            print("Se agrego el producto ",a," correctamente.")
            
        elif str[1] == 'compra':
            print("")
        #print(f'Mensaje recibido de {addr}: {received_message}')
        
        # Almacenar mensaje recibido en un archivo
        with open(f"/home/eduardo/msgs.txt", "a") as file:
            file.write(f"[Recibido] {time.strftime('%Y-%m-%d_%H:%M:%S')} - {received_message}\n")
        
        # Enviar un mensaje de confirmación al cliente
        confirmation_message = "El mensaje fue recibido"
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
        t = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
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
            file.write(f"[Recibido] {time.strftime('%Y-%m-%d_%H:%M:%S')} - {decoded_response}\n")

def obtener_uuid():
    try:
        # Ejecutar el comando dmidecode para obtener la información del sistema
        proceso = subprocess.Popen(['sudo', 'dmidecode', '-s', 'system-uuid'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        salida, errores = proceso.communicate()

        if proceso.returncode == 0:
            # Si el comando se ejecutó con éxito, se imprime el UUID
            return salida.strip()
        else:
            # Si hay errores, se imprime un mensaje de error
            print(f"Error al ejecutar dmidecode: {errores}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":    
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
    j = -1
    uuid = obtener_uuid()
    while (i < idP):
        cur.execute('SELECT total FROM PRODUCTO WHERE idProducto = ?',(i, ))
        a = cur.fetchone()
        n = a[0]
        m = len(hosts)
        t = [n//m]*m
        r = n % m
        for x in range(r):
            t[x] += 1
        if (uuid == names[0]):
            j = 1
        elif (uuid == names[1]):
            j = 2
        elif (uuid == names[2]):
            j = 3
        elif (uuid == names[3]):
            j = 4
        cur.execute('INSERT INTO INVENTARIO (idSucursal, producto, cantidad) VALUES (?,?,?)',(j,i,t[j-1]))
        i += 1
    bd.commit()

#if __name__ == "__main__":
    # Configuración de los servidores en cada máquina virtual
    #hosts = [
        #"192.168.153.128",
        #"192.168.153.129",
        #"192.168.153.130",
        #"192.168.153.131"
    #]
    #port = [      # Puerto para la comunicación entre las máquinas
        #1111,
        #2222,
        #3333,
        #4444
    #]
    # Iniciar los servidores en cada máquina virtual
    #vm1 = threading.Thread(target=servidor, args=(hosts[0], port[0]))
    #vm1.start()
    #vm2 = threading.Thread(target=servidor, args=(hosts[1], port[1]))
    #vm2.start()
    #vm3 = threading.Thread(target=servidor, args=(hosts[2], port[2]))
    #vm3.start()
    #vm4 = threading.Thread(target=servidor, args=(hosts[3], port[3]))
    #vm4.start()

    # Menú del cliente para enviar mensajes
    #while True:
        #print("\nSeleccione a qué servidor desea enviar un mensaje:")
        #for i, host in enumerate(hosts, start=1):
            #print(f"{i}. {host}")

        #choice = input("Ingrese el número correspondiente al servidor o '0' para salir: ")
        #if choice == '0':
            #break

        #try:
            #choice_idx = int(choice) - 1
            #if 0 <= choice_idx < len(hosts):
                #server_ip = hosts[choice_idx]
                #port_i = port[choice_idx]
                #message = input("Ingrese el mensaje a enviar: ")
                #mensaje(server_ip, port_i, message)
            #else:
                #print("Opción inválida. Intente de nuevo.")
        #except ValueError:
            #print("Entrada inválida. Ingrese un número válido o '0' para salir.")
