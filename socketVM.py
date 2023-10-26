import os 
import socket
import threading

VM1 = '192.168.229.129'
VM2 = '192.168.229.130'
VM3 = '192.168.229.131'
VM4 = '192.168.229.132'
VM5 = '192.168.229.133'
PORT = 8000
clk = 0

s = socket.socket()
s.bind((VM1,PORT))
s.bind((VM2,PORT))
s.bind((VM3,PORT))
s.bind((VM4,PORT))
s.bind((VM5,PORT))

def envia(vm,m,b):
    s.connect((vm, PORT))
    mt = m + " en tmp= " + clk
    s.sendto(mt.encode('utf-8'),vm)
    print("Mensaje enviado para ",vm,": ",mt)
    b.write("Mensaje enviado para " + vm + ": " + mt + os.linesep)

def recibe(b):
    s.listen(1)
    d, vm = s.accept()
    print("Mensaje recibido de ",vm,": ",d.decode('utf-8'))
    b.write("Mensaje recibido de " + vm + ": " + d.decode('utf-8') + os.linesep)

def main():
    if(not(os.path.exists('/home/eduardo/SD/bitacora.txt'))):
        b = open("/home/eduardo/SD/bitacora.txt", "w")
    print("Middleware...")
    while True:
        cmd = input("<> ")
        if (cmd == 'e'):
            mensaje = input("Escribe el mensaje a enviar<> ")
            opc = input("A que nodo desea enviar el mensaje? <> ")
            match opc:
                case 1:
                    envia(VM1,mensaje,b)
                case 2:
                    envia(VM2,mensaje,b)
                case 3:
                    envia(VM3,mensaje,b)
                case 4:
                    envia(VM4,mensaje,b)
                case 5:
                    envia(VM5,mensaje,b)
        elif (cmd == 's'):
            b.close()
            return
        else:
            recibe(b)
        clk += 1

if __name__ == "__main__":
    main()

####### SERVIDOR ##########

clientes = []
#Funcion para manejar una conexion de cliente 
def conexion(sCliente): 
    while True:
        data = sCliente.recv(1024) 
        if not data:
            break 
    mensaje = data.decode()
    print (f"Mensaje del cliente: {mensaje}")
#Enviar confirmacion al cliente confirmacion = "Mensaje recibido" Scliente.send(confirmacion.encode())
    sCliente.close()

#Configuracion nodo servidor 
host = '0.0.0.0' 
#escucha culquier interfaz de red 
puerto = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,puerto))
server.listen(5)
print (f"Servidor escuchando en {host}:{puerto}")

#Conexiones entrantes

while True:
    sCliente, addr= server.accept()
    print (f"Conexion entrante de: faddr [0]): {addr [1]}")
    clientes.append(sCliente)
    cThread = threading. Thread (target = conexion, args = (sCliente,))
    cThread.start()

######## CLIENTE ######

#Funcion control de mensajes 

def recibir_mensajes (cliente): 
    while True:
        data =cliente.recv(1024) 
        if not data: 
            break
        mensaje = data.decode() 
        print (f"Respuesta del servidor: {mensaje}")

#configuracion del cliente host='192.168.171.129

puerto = 8888

#Creando el socket del cliente 
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conectarse al servidor 
cliente.connect((host, puerto))

#Hilo para el control de mensajes 
h_rec = threading.Thread(target = recibir_mensajes, args = (cliente,))
h_rec.start()

while True:
    mensaje = input("Escribe un mensaje o (q) para cerrar la conexion: ")
    if mensaje. Lower() == 'q':
        break

#Escribir el mensaje y guardar el mensaje en un archivo de texto 
with open("misMensajes.txt", "a") as archivo: 
    archivo.urite(mensaje + "\n")

#Enviar el mensaje 
cliente.send(mensaje.encode())

#Recibir
respuesta = cliente.recv(1024) 
print (f"Respuesta del servidor: {respuesta.decode()}")

#Cerrar 
conexion = cliente.close()