import socket

SERVER_HOST = socket.gethostname()
SERVER_PORT = 8000
BUFFER_SIZE = 1024


chat_id = input("Идентификатор чата ").strip()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))
client.send(chat_id.encode())


while True:
    message = input("Сообщение ").strip()
    client.send(message.encode())
    if message == "exit":
        break

client.close()
