import socket
import threading

# Función para manejar las conexiones entrantes como servidor
def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Recibido: {data.decode('utf-8')}")
        client_socket.send("Mensaje recibido".encode('utf-8'))
    client_socket.close()

# Función para enviar mensajes como cliente a una dirección IP específica
def send_message(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    while True:
        message = input("Escribe un mensaje: ")
        client.send(message.encode('utf-8'))
        response = client.recv(1024)
        print(f"Respuesta del servidor: {response.decode('utf-8')}")

# Configuración del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))
server.listen(5)

print("Servidor escuchando en el puerto 12345")

# Iniciar un hilo para el servidor
server_thread = threading.Thread(target=handle_client, args=(server.accept()[0],))
server_thread.start()

# Permite al usuario especificar la dirección IP y puerto del cliente
client_ip = input("Ingresa la dirección IP del cliente: ")
client_port = int(input("Ingresa el puerto del cliente: "))

# Iniciar un hilo para el cliente
client_thread = threading.Thread(target=send_message, args=(client_ip, client_port))
client_thread.start()
