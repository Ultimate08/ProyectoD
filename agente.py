from collections import namedtuple
import socket
import threading
import datetime

# Configura las IP de tus nodos
nodos = [
    {'host': '192.168.229.128', 'port': 12345},
    {'host': '192.168.229.129', 'port': 12346},
    {'host': '192.168.229.134', 'port': 12347},
    {'host': '192.168.229.135', 'port': 12348}
]

b = open("/home/eduardo/SD/bitacora.txt", "w") # Cambien la ruta y creen el archivo

def server(n):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((n['host'], n['port']))
        server_socket.listen()
        print(f"Servidor escuchando en {n['host']}:{n['port']}")
        conn, addr = server_socket.accept()

        with conn:
            print(f"Conexión establecida desde {addr}")

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Mensaje recibido del cliente: {data.decode('utf-8')}")
                b.write("\n"+data.decode('utf-8'))
                response = "El mensaje ha sido recibido\n"
                conn.sendall(response.encode('utf-8'))

def client(n):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((n['host'], n['port']))
        while True:
            message = input("Escribe un mensaje para el servidor: ")
            tmp = str(datetime.datetime.now())
            msg = message+" "+tmp
            client_socket.sendall(msg.encode('utf-8'))
            data = client_socket.recv(1024)
            b.write("\n"+msg)
            print(f"Respuesta del servidor: {data.decode('utf-8')}")

print("Elige un servidor:")
for i, n in enumerate(nodos):
    print(f"{i + 1}. {n['host']}:{n['port']}")

choice = int(input("Selecciona el número del servidor: ")) - 1

# Crear y ejecutar hilos para el servidor y el cliente
server_thread = threading.Thread(target=server, args=(nodos[choice],))
client_thread = threading.Thread(target=client, args=(nodos[choice],))

server_thread.start()
client_thread.start()

server_thread.join()
client_thread.join()
