import socket


HOST = (socket.gethostname(), 8000)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:

    client_socket.connect(HOST)

    request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(socket.gethostname())
    client_socket.sendall(request.encode())


    response = client_socket.recv(1024)
    print(f"Ответ от сервера: {response.decode()}")

except Exception as e:
    print(f"Ошибка: {e}")


