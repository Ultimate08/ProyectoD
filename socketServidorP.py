import socket
import threading

host = 'localhost'
puerto = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Utilizando un socket de internet con el protocolo TCP
server.bind( (host, puerto) ) #Pasar datos de conexion
server.listen()
print(f"Servidor corriendo en {host} : {puerto}")

clientes = [] #Almacenar conexion de los usuarios


def broadcast(mensaje, _cliente):
    for clientes in clientes:
        if cliente != _cliente:
            cliente.send(mensaje)


def handle(cliente):  #Funcion para controlar los mensajes que son enviados
    while True:
        try:
            mensaje = cliente.recv(1024) #para recibir los mensajes
            broadcast(mensaje, cliente)
        except:
            index = clientes.index(cliente)
            usr = nicks[index]
            broadcast(f"Server: {usr} desconectado".encode())
            clientes.remove(cliente)
            nicks.remove(usr)
            cliente.close()
            break

def conexiones():
    while True:
        cliente, addr = server.accept() #retorna el objeto del cliente, despues el IP y el puerto
        clientes.append(cliente)
        print(f"Se conecto: {cliente} desde: {str(addr)}")

        threading.Thread(target = handle, args = (cliente,))
        thread.start()


conexiones()