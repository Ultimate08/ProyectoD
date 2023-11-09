import socket
import threading

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Mensaje recibido: {data.decode()}")

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    client_receive_thread = threading.Thread(target=handle_client, args=(client,))
    client_receive_thread.start()

    while True:
        message = input("Ingrese un mensaje: ")
        client.send(message.encode())

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Servidor escuchando en el puerto 5555...")

    while True:
        client, addr = server.accept()
        print(f"Conexion entrante desde {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

server_thread = threading.Thread(target=start_server)
client_thread = threading.Thread(target=start_client)

server_thread.start()
client_thread.start()
