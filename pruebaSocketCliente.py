import socket

# Configurar el cliente
host = '127.0.0.1'  # Dirección IP del servidor
puerto = 8888

# Crear un socket de cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarse al servidor
cliente.connect((host, puerto))

while True:
    mensaje = input("Escribe un mensaje (o 'salir' para cerrar la conexión): ")
    if mensaje.lower() == "salir":
        break

    # Enviar el mensaje al servidor
    cliente.send(mensaje.encode())

    # Recibir y mostrar la respuesta del servidor
    respuesta = cliente.recv(1024)
    print(f"Respuesta del servidor: {respuesta.decode()}")

# Cerrar la conexión
cliente.close()
