import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 9090))

question = client_socket.recv(1024).decode() #вопрос от сервера 
print(question)

abh = input()

client_socket.send(abh.encode()) #отправляем данные серверу

result = client_socket.recv(1024).decode()
print(result)

client_socket.close()
