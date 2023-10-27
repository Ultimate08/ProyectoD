import socket
import threading

class Server:
    def __init__(self, host='192.168.1.68', port=8888):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.nicknames = []

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f'{nickname} left the chat!'.encode())
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')

            client.send('NICK'.encode())
            nickname = client.recv(1024).decode()
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f'Nickname of client is {nickname}!')
            self.broadcast(f'{nickname} joined the chat!'.encode())
            client.send('Connected to the server!'.encode())

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

if __name__ == '__main__':
    server = Server()
    server.receive()