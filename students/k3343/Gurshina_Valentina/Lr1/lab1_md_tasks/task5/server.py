import socket
import threading
import urllib.parse #библиотека для декодирования данных

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8081  # порт для работы сервера
grades_data = {}  # хранение оценок

def process_client_request(client_socket, client_address):
    request = client_socket.recv(1024).decode('utf-8') 
    request_parts = request.split(' ')

    if len(request_parts) >= 3:
        method, path, protocol = request_parts[:3]
        print(f"Получен запрос методом {method} от {client_address}")

        if method == 'GET':
            send_http_response(client_socket, '200 OK', 'Content-Type: text/html; charset=utf-8', generate_html())
        elif method == 'POST':
            content_length = int(request.split('Content-Length: ')[1].split('\r\n')[0])
            body = request.split('\r\n\r\n', 1)[1]
            while len(body.encode('utf-8')) < content_length:
                body += client_socket.recv(1024).decode('utf-8')  
            post_params = extract_post_parameters(body)
            discipline, grade = post_params.get('discipline', ''), post_params.get('grade', '')
            grades_data[discipline] = grades_data.get(discipline, []) + [grade]
            send_http_response(client_socket, "200 OK", "Content-Type: text/html; charset=utf-8", generate_html())
        else:
            send_http_response(client_socket, '405 Method Not Allowed', 'Content-Type: text/plain; charset=utf-8',
                               'This method is not allowed. Try again, please ^.^')
    else:
        send_http_response(client_socket, '400 Bad Request', 'Content-Type: text/plain; charset=utf-8', 'Failed Request')
    client_socket.close()

def send_http_response(client_socket, status_code, content_type, body_content):
    response = f"""HTTP/1.1 {status_code}
{content_type}
Content-Length: {len(body_content.encode("utf-8"))}

{body_content}
"""
    client_socket.sendall(response.encode('utf-8'))  

def extract_post_parameters(post_data):
    post_data = post_data.replace('+', ' ') # замена + на пробелы
    return {key: urllib.parse.unquote(value, encoding='utf-8') for key, value in
            [item.split('=') for item in post_data.split('&')]}

def generate_html():
    rows = "".join(
        [f"<tr><td>{discipline}</td><td>{','.join(grades)}</td></tr>" for discipline, grades in grades_data.items()]
    )
    return f"""<!DOCTYPE html>
<html>
<head>
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
 <title>Отметки</title>
</head>
<body>
<form method="POST">
 <input type="text" id="discipline" name="discipline" placeholder="Дисциплина" required>
 <input type="number" id="grade" name="grade" min="1" max="5" placeholder="Оценка" style="width: 60px;" required>
 <button type="submit">Отправить</button>
</form>
 <h1>Отметки</h1>
 <table border="1">
 <tr><th>Дисциплина</th><th>Отметки</th></tr>
 {rows}
 </table>
</body>
</html>"""

# осн функция для запуска сервера
def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen()
        print(f"Запуск сервера на порту {SERVER_PORT}")
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=process_client_request, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    run_server()
