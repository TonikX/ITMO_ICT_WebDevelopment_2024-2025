import socket
from threading import Thread
from colorama import Fore, init
init()

HOST = '127.0.0.1'
PORT = 16000
client_sockets = set()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
print(f'{Fore.YELLOW}Starting server - {HOST}:{PORT}{Fore.RESET}')
server.listen()

def listen_for_client(client, addr):
    while True:
        try:
            msg = client.recv(1024).decode()
        except ConnectionResetError:
            print(f'{Fore.GREEN}Disconnected - {addr[0]}:{addr[1]}{Fore.RESET}')
            client_sockets.remove(client)
            break
        except Exception as e:
            print(f'Internal error: {e}')
            client_sockets.remove(client)
            break
        for socket in client_sockets:
            socket.sendall(msg.encode())

while True:
    try:
        cl_socket, cl_addr = server.accept()
        print(f'{Fore.GREEN}Connected - {cl_addr[0]}:{cl_addr[1]}{Fore.RESET}')
        client_sockets.add(cl_socket)
        t = Thread(target=listen_for_client, args=(cl_socket, cl_addr, ))
        t.daemon = True
        t.start()
    except KeyboardInterrupt:
        break

for sock in client_sockets:
    sock.close()

print(f'{Fore.YELLOW}Shutting server... {Fore.RESET}')
server.close()
        