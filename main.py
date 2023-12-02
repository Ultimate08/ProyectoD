from servidor import servidor, hilo_servidor
from cliente import cliente, hilo_cliente

def main():
    #Crear el servidor y los hilos para los clientes
    s = servidor()
    s.iniciar()


main()



'''
from servidor import start_server
from cliente import start_client

def main():
    # Iniciar el servidor en un hilo separado
    server_thread = start_server()

    # Iniciar el cliente
    start_client()

    # Esperar a que el hilo del servidor termine (puede omitirse si no es necesario)
    server_thread.join()

if __name__ == "__main__":
    main()
'''