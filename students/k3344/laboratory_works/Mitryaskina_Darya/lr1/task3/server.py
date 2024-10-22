import socket

def handle_request(client_socket):
    # Чтение запроса от клиента
    request = client_socket.recv(1024).decode()
    print(f"Получен запрос:\n{request}")

    # Формирование ответа
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += "Content-Length: {}\r\n".format(len(html_content))
    response += "\r\n"
    response += html_content

    client_socket.sendall(response.encode())

    client_socket.close()

with open("task3/index.html", "r", encoding="utf-8") as file:
    html_content = file.read()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))

server_socket.listen(5)
print("Сервер запущен на порту 8080")

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключен клиент: {addr}")

        handle_request(client_socket)
finally:
    server_socket.close()