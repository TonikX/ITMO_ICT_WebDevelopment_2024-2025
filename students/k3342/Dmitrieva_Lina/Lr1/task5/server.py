import socket
import threading
import urllib.parse

grades = []

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    headers = request.split('\n')

    if len(headers) > 0 and len(headers[0].split()) >= 2:
        method, path = headers[0].split()[:2]
        
        if method == 'GET':
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            response += """
            <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Оценки</title>
                </head>
                <body>
                    <h2>Введите дисциплину и оценку</h2>
                    <form action="/" method="POST">
                        <label for="subject">Дисциплина:</label><br>
                        <input type="text" id="subject" name="subject"><br>
                        <label for="grade">Оценка:</label><br>
                        <input type="text" id="grade" name="grade"><br><br>
                        <input type="submit" value="Отправить">
                    </form>
                    <h2>Все оценки:</h2>
                    <ul>
            """
            for subject, grade in grades:
                response += f"<li>{subject}: {grade}</li>"
            response += "</ul></body></html>"

            client_socket.send(response.encode('utf-8'))

        elif method == 'POST':
            body = request.split('\r\n\r\n')[1]
            params = {param.split('=')[0]: urllib.parse.unquote(param.split('=')[1]) for param in body.split('&')}
            
            subject = params['subject']
            grade = params['grade']
            grades.append((subject, grade))

            response = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"
            client_socket.send(response.encode())

    client_socket.close()

def start_server():
    server_address = ('localhost', 8080)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen()

    print(f"Сервер запущен и ожидает подключения на порту {server_address[1]}...")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
