import socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    HOST, PORT = 'localhost', 1235
    s.connect((HOST, PORT))
    data = s.recv(1024)
    print("Получено от сервера:")
    print(data.decode('utf-8'))
    s.close()



