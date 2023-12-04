import socket
import threading
import time
import sqlite3
import random

def cliente(conn, addr):
    print(f'Conectado por {addr}')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        received_message = data.decode()
        print(f'Mensaje recibido de {addr}: {received_message}')
        
        # Almacenar mensaje recibido en un archivo
        with open(f"/home/eduardo/msgs.txt", "a") as file:
            file.write(f"[Recibido] {time.strftime('%Y-%m-%d %H:%M:%S')} - {received_message}\n")
        
        # Enviar un mensaje de confirmación al cliente
        confirmation_message = "Recibido"
        conn.sendall(confirmation_message.encode())
        print(f'Mensaje de confirmación enviado a {addr}: {confirmation_message}')

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
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        mt = f"[{t}] {message}"
        s.sendall(mt.encode())
        print(f"Mensaje enviado a {server_ip}:{server_port}: {mt}")
        
        # Almacenar mensaje enviado en un archivo
        with open(f"client_messages.txt", "a") as file:
            file.write(f"[Enviado] {t} - {message}\n")
        
        response = s.recv(1024)
        decoded_response = response.decode()
        print(f"Respuesta del servidor {server_ip}:{server_port}: {decoded_response}")
        
        # Almacenar mensaje de confirmación recibido en un archivo
        with open(f"/home/eduardo/msgs.txt", "a") as file:
            file.write(f"[Recibido] {time.strftime('%Y-%m-%d %H:%M:%S')} - {decoded_response}\n")

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


def crearDB():
    # Conectar a la base de datos (creará la base de datos si no existe)
    conn = sqlite3.connect('tienda_libros.db')

    # Crear un objeto cursor
    cursor = conn.cursor()

    # Crear una tabla de libros (si no existe)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY,
            titulo TEXT,
            autor TEXT,
            precio REAL
        )
    ''')

    # Insertar datos de ejemplo en la tabla de libros
    libros_data = [
        ('El señor de los anillos', 'J.R.R. Tolkien', 25.99),
        ('Cien años de soledad', 'Gabriel García Márquez', 19.99),
        ('1984', 'George Orwell', 15.50),
        ('Harry Potter y la piedra filosofal', 'J.K. Rowling', 22.75),
    ]

    cursor.executemany("INSERT INTO libros (titulo, autor, precio) VALUES (?, ?, ?)", libros_data)

    # Guardar (commit) los cambios
    conn.commit()

    # Consultar datos
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()

    # Mostrar los datos
    print("Libros en la tienda:")
    for libro in libros:
        print(f"ID: {libro[0]}, Título: {libro[1]}, Autor: {libro[2]}, Precio: ${libro[3]:.2f}")

    # Cerrar la conexión
    conn.close()
