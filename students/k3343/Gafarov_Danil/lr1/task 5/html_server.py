import socket
from urllib.parse import unquote_plus

grades = []
#Генерация html по данным из массива grades
def generate_html():
    html = "<html><head><meta charset='UTF-8'><title>Оценки по дисциплинам</title></head><body>"
    html += "<h1>Оценки по дисциплинам</h1><ul>"
    subjects = {}
    for grade in grades:
        subject = grade['subject']
        score = grade['score']
        if subject in subjects:
            subjects[subject].append(score)
        else:
            subjects[subject] = [score]

    # Вывод оценок
    for subject, scores in subjects.items():
        html += f"<li>{subject}: {', '.join(scores)}</li>"
    html += "</ul>"
    html += '''
        <h2>Добавить оценку</h2>
        <form method="POST">
            <label>Дисциплина: <input type="text" name="subject"></label><br>
            <label>Оценка: <input type="text" name="score"></label><br>
            <input type="submit" value="Добавить">
        </form>
    '''
    html += "</body></html>"
    return html

def parse_post_data(data):
    post_data = {}
    params = data.split('&')
    for param in params:
        key, value = param.split('=')
        post_data[key] = unquote_plus(value)
    return post_data

def handle_request(request):
    headers, _, body = request.partition('\r\n\r\n')
    lines = headers.splitlines()
    request_line = lines[0]
    method, path, _ = request_line.split()

    if method == 'GET':
        response_body = generate_html()
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n' + response_body
        return response

    elif method == 'POST':
        post_data = parse_post_data(body)
        grades.append({'subject': post_data.get('subject', ''), 'score': post_data.get('score', '')})
        response_body = generate_html()
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n' + response_body
        return response

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = 'localhost'
    PORT = 8080
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Сервер запущен на порту http://{HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Получен запрос от {addr}")

        request = client_socket.recv(1024).decode('utf-8')
        if request:
            response = handle_request(request)
            client_socket.sendall(response.encode('utf-8'))

        client_socket.close()

if __name__ == '__main__':
    start_server()