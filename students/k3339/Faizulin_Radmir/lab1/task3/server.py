import socket

def load_html(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<html><body><h1>Ошибка 404: Файл не найден</h1></body></html>"

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 8080)
serverSock.bind(server_address)
serverSock.listen(1)
print("Сервер запущен и ожидает подключения...")

while True:
    connection, client_address = serverSock.accept()
    try:
        print(f"Подключение от клиента: {client_address}")

        request = connection.recv(1024).decode()
        print(f"Получен HTTP-запрос: {request}")
        # читка
        html_content = load_html("index.html")

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(html_content)}\r\n"
            "\r\n"
            f"{html_content}"
        )
        # jnghfdrf овтета клиенту
        connection.sendall(response.encode())
    finally:
        connection.close()
        print(f"Соединение с {client_address} закрыто.")

#  http://127.0.0.1:8080/