import socket
import threading

# Función para revisar y contestar el mensaje recibido
def manejar_conexion(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        # Procesar los datos recibidos
        respuesta = "Respuesta: " + data.decode()
        client_socket.send(respuesta.encode())
    client_socket.close()


def enviar_mensaje(ip, puerto, mensaje):
    try:
        nodo = (ip, puerto)
        server.sendto(mensaje.encode(), nodo)
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")


# Configurar el servidor
host = '0.0.0.0'  # Escuchar en todas las interfaces de red
puerto = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, puerto))
server.listen(5)
print(f"Servidor escuchando en {host}:{puerto}")

# Esperar y manejar conexiones entrantes en hilos
while True:
    client_socket, addr = server.accept()
    print(f"Conexión entrante desde {addr[0]}:{addr[1]}")

    # Crear un hilo para manejar la conexión del cliente
    cliente_thread = threading.Thread(target=manejar_cliente, args=(client_socket,))
    cliente_thread.start()

    #Obtener la direccion IP y el puerto a los que se enviara el mensaje
    ip_destino = input("Ingrese la direccion IP del nodo destino: ")
    mensaje = input("Ingrese el mensaje a enviar: ")

    #Enviar el mensaje al nodo destino
    enviar_mensaje(ip_destino, puerto, mensaje)