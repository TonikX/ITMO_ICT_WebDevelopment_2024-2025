import socket
import threading

HOST = 'localhost'
PORT = 9090

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive_message():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'nickname':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Disconnected from server.")
            client.close()
            break


def write_message():
    while True:
        text = input()

        if text == "/quit":
            client.send(f"{nickname} left the chat.".encode('utf-8'))
            client.close()
            break
        else:
            message = f"{nickname}: {text}"
            client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_thread = threading.Thread(target=write_message)
write_thread.start()
