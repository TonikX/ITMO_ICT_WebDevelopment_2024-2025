import socket
import threading

PORT = 1313
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(BUFFER_SIZE)
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            break

def receive():
    while True:
        print('Server is running and listening...')
        client, addr = server.accept()
        print(f'Connection is established with {str(addr)}')
        clients.append(client)
        broadcast(f'{str(addr)} has entered the room\n'.encode(FORMAT), None)  # Notify all about new connection
        client.send('You are now connected'.encode(FORMAT))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
