import socket
import threading


def get_text(client_socket):
    while True:
        try:
            other_text = client_socket.recv(1024).decode()
            if other_text:
                print(str(other_text))
            else:
                break
        except:
            break


cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_address = ('localhost', 8080)
cl_socket.connect(serv_address)

thread = threading.Thread(target=get_text, args=(cl_socket, ))
thread.start()

while True:
    text = input("")
    cl_socket.send(text.encode())
    if text == 'leave':
        cl_socket.close()
        break
