import socket
import threading

nickname = str(input("Enter your nickname: "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))


def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'YOU_HAVE_JOINED_THE_CHAT!':
                client_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Error")
            client_socket.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client_socket.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()