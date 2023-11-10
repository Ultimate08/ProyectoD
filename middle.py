import socket
import threading

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Mensaje recibido: {data.decode()}")

#Parte del codigo que indica a que socket se quiere conectar
def start_client():
    #Digitar a que socket desea mandarle mensaje
    addr = input("address: \n")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('addr', 5555))

    client_receive_thread = threading.Thread(target=handle_client, args=(client,))
    client_receive_thread.start()

    while True:
        mensaje = input("Ingrese un mensaje: ")
        with open("misMensajes.txt", "a") as archivo:
            archivo.write(mensaje + "\n")
        client.send(mensaje.encode())

#Parte de codigo que indica por que direccion y puerto va a estar escuchando el socket
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.74.222', 5555))
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
server_thread.join()
client_thread.start()
