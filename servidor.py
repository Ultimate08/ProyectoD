import socket
import threading


class hilo_servidor(threading.Thread):
    def __init__(self, conexion, direccion, sockets):
        threading.Thread.__init__(self)
        self.conexion = conexion
        self.direccion = direccion
        self.sockets = sockets
    
    def run(self):            
        while True:
            data = self.conexion.recv(2048)
            dt = data.decode()
            if (dt == ''):
                continue
            print(self.direccion[0], " > ", dt)

class servidor():
    def iniciar():
        cliente_sockets = []
        hilos = []
        socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_servidor.bind(('0.0.0.0', 8888))
        socket_servidor.listen(3) #Permite escuchar 3 conexiones
        print("\nSocket creado, escuchando desde [192.168.74.222] y en el puerto [8888]")


        while True:
            #metodo para que acepte conexiones
            conexion_socket, direccion = socket_servidor.accept()
            print("Primera conexion desde: ", direccion[0])
            hilo = hilo_servidor(conexion_socket, direccion, cliente_sockets)
            hilo.start()
            hilos.append(hilo)
            cliente_sockets.append(conexion_socket)

servidor.iniciar()
