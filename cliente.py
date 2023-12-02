import socket
import threading


class hilo_cliente(threading.Thread):
    def __init__(self, socket, ip, puerto):
        self.socket = socket
        self.ip = ip
        self.puerto = puerto
    def run(self):
        while True:
            data = socket.recv(2048)
            dt = data.decode()
            if(dt == ''):
                continue
            print("dt")

class cliente():
    def iniciar():
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("\nSocket cliente creado...")
        socket_cliente.connect(('192.168.153.128', 8888))
        print("\nEl socket del cliente se conecto al servidor")
        h1 = hilo_cliente(socket_cliente)
        h1.start()
        while True:
            data = input("Ingrese el mensaje al servidor: ")
            dt = data.encode()
            socket_cliente.send(dt)


# cliente.iniciar()
