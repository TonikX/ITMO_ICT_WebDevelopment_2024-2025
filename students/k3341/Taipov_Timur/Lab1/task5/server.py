import socket
import threading
import urllib.parse

grades = {}


def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')

    headers = request.split('\r\n')
    first_line = headers[0]
    method, path, _ = first_line.split()

    if method == "POST" and path == "/grades":
        content = headers[-1]
        content = content.split('&')
        discipline = urllib.parse.unquote(content[0][11:])
        grade = urllib.parse.unquote(content[1][6:])
        grades[discipline] = grades.get(discipline, []) + [grade]

        print(grades)
        response = "HTTP/1.1 303 See Other\r\nLocation: /grades\r\n\r\n"
        client_socket.sendall(response.encode())

    elif method == "GET" and path == "/grades":
        response_body = """
        <html>
        <head><title>Оценки</title></head>
        <body>
        <h1>Оценки по дисциплинам</h1>
        <ul>
        """
        for discipline in grades:
            response_body += f"<li>{discipline}: {', '.join(map(str, grades.get(discipline, [])))}</li>"
        response_body += """
        </ul>
        <h2>Добавить оценку</h2>
        <form method="post" action="/grades">
            Дисциплина: <input type="text" name="discipline"><br>
            Оценка: <input type="text" name="grade"><br>
            <input type="submit" value="Добавить">
        </form>
        </body>
        </html>
        """

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(response_body.encode())}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{response_body}"
        )

        client_socket.sendall(response.encode('utf-8'))

    client_socket.close()


def start_server(host="localhost", port=8085):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_sock, _ = server_socket.accept()
        handle_client(client_sock)



if __name__ == "__main__":
    start_server()