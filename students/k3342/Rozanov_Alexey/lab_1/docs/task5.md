# Задание 5

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

## Файл server.py

Код:

```python
import socket
from urllib.parse import parse_qs

global grades
grades = []


def load_html():
    """
    html loader
    :return: readed file
    """
    with open("/Users/alexr/Documents/study/sem5/web_prog/ITMO_ICT_WebDevelopment_2024-2025/students/k3342/Rozanov_Alexey/lab_1/task_5/index.html", 'r') as file:
        return file.read()


def handle_request(request):
    """
    requests handler
    :param request:
    :return: func generate_response
    """
    headers, body = request.split("\r\n\r\n")
    lines = headers.split("\r\n")
    method, path, _ = lines[0].split(" ")

    if method == "GET":
        response_body = load_html('index.html')
        return generate_response(200, response_body)

    elif method == "POST":
        content_length = int([line.split(": ")[1] for line in lines if line.startswith("Content-Length")][0])
        post_data = body[:content_length]
        form_data = parse_qs(post_data)
        subject = form_data.get("subject", [""])[0]
        grade = form_data.get("grade", [""])[0]
        if subject and grade:
            grades.append((subject, grade))

        response_body = load_html('index.html')
        grades_html = "".join([f"<li>{subject}: {grade}</li>" for subject, grade in grades])
        response_body = response_body.replace("<ul id=\"grades\">", f"<ul id=\"grades\">{grades_html}")

        return generate_response(200, response_body)


def generate_response(status_code, body):
    """
    response generator: makes full response with header
    :param status_code: response status code
    :param body: response body
    :return: generated full response
    """
    status_message = {200: "OK", 404: "Not Found"}.get(status_code, "OK")
    response = f"HTTP/1.1 {status_code} {status_message}\r\n"
    response += "Content-Type: text/html; charset=UTF-8\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    response += "\r\n"
    response += body
    return response


def run_server(host='127.0.0.1', port=8088):
    """
    server starter and worker
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server is listening on port 8058...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        request = client_socket.recv(1024).decode('utf-8')
        if request:
            response = handle_request(request)
            client_socket.sendall(response.encode('utf-8'))

        client_socket.close()


if __name__ == "__main__":
    run_server()
```

Скриншот работы сервера:

[server works](imgs/task5_server.png)

## Файл index.html

Код:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grades</title>
</head>
<body>
    <h1>Submit your grade</h1>
    <form action="/" method="post">
        <label for="subject">Subject:</label><br>
        <input type="text" id="subject" name="subject"><br>
        <label for="grade">Grade:</label><br>
        <input type="text" id="grade" name="grade"><br><br>
        <input type="submit" value="Submit">
    </form>
    <h2>Grades</h2>
    <ul id="grades">
        <!-- Grades will be displayed here -->
    </ul>
</body>
</html>

```

Скриншоты работы сервера (веб):

[Скриншот до записи](imgs/task5_web1.png)

[Скриншот после записи](imgs/task5_web2.png)