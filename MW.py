import socket
import threading

def cliente(conn, addr):
    print(f'Conectado por {addr}')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f'Mensaje recibido de {addr}: {data.decode()}')
        # Aquí puedes procesar el mensaje como desees

    conn.close()

def servidor(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print(f"Servidor escuchando en {host}:{port}")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=cliente, args=(conn, addr))
            client_thread.start()

def mensaje(server_ip, server_port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        s.sendall(message.encode())
        print(f"Mensaje enviado a {server_ip}:{server_port}: {message}")

if __name__ == "__main__":
    # Configuración de los servidores en cada máquina virtual
    hosts = [
        "192.168.153.128",
        "192.168.153.129",
        "192.168.153.130",
        "192.168.153.131"
    ]
    port = 12345  # Puerto para la comunicación entre las máquinas

    # Iniciar los servidores en cada máquina virtual
    for host in hosts:
        server_thread = threading.Thread(target=servidor, args=(host, port))
        server_thread.start()

    # Menú del cliente para enviar mensajes
    while True:
        print("\nSeleccione a qué servidor desea enviar un mensaje:")
        for i, host in enumerate(hosts, start=1):
            print(f"{i}. {host}")

        choice = input("Ingrese el número correspondiente al servidor o 'q' para salir: ")
        if choice.lower() == 'q':
            break

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(hosts):
                server_ip = hosts[choice_idx]
                message = input("Ingrese el mensaje a enviar: ")
                mensaje(server_ip, port, message)
            else:
                print("Opción inválida. Intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingrese un número válido o 'q' para salir.")
