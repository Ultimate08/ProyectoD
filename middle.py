import socket
import threading

def send_msg(client_socket):
    while True:
        msg = input("")
        client_socket.send(msg.encode())
        if msg == "{quit}":
            break

def receive_msg(client_socket):
    while True:
        msg = client_socket.recv(1024).decode()
        print(msg)
        if msg == "{quit}":
            break

def create_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))

    send_thread = threading.Thread(target=send_msg, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_msg, args=(client_socket,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    client_socket.close()

if __name__ == "__main__":
    create_client()