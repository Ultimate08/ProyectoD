import socket
import threading

host = '192.168.1.68'
port = 8888

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect( (host, port) )


def recibir_mensaje():
    while True:
        try:
            cliente.recv(1024).decode()
        except:
            break


def enviar_mensaje():
    while True:
        mensaje = f"{addr}: {imput('')}"
        cliente.send(mensaje.encode())

th_recibir = threading.Thread(target = recibir_mensaje)
th_recibir.start()
th_enviar = threading.Thread(target = enviar_mensaje)
th_enviar.start()
