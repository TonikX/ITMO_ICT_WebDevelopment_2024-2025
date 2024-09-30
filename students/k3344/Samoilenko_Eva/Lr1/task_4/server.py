import socket
import threading

clients = []
names = []


def client_handler(client_socket):
    while True:
        try:
            text = client_socket.recv(1024).decode()
            if text == 'leave':
                leave_chat(client_socket)
            elif text:
                print(str(text))
                send_text(text, client_socket)
        except:
            continue


def send_text(text, client_socket):
    for client in clients:
        if client != client_socket:
            index = clients.index(client_socket)
            name = names[index]
            client.send(f'{name}: {text}'.encode())


def leave_chat(client_socket):
    send_text('has abandoned y\'all', client_socket)
    ind = clients.index(client_socket)
    clients.remove(client_socket)
    name = names[ind]
    names.remove(name)
    print(f'{name} left')


serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_address = ('localhost', 8080)
serv_sock.bind(serv_address)
serv_sock.listen()
print('server is connected and listening:', serv_address)

while True:
    cl_socket, cl_address = serv_sock.accept()
    cl_socket.send('what\'s your name:'.encode())
    name = cl_socket.recv(1024).decode()
    names.append(name)
    clients.append(cl_socket)
    print(f'{name} joined')
    send_text('is amongst you now', cl_socket)

    thread = threading.Thread(target=client_handler, args=(cl_socket, ))
    thread.start()
