import socket
from urllib.parse import parse_qs

grades = []

def load_html(): 
    with open("/Users/veronikanevzorova/Desktop/web/ITMO_ICT_WebDevelopment_2024-2025/task_3/index.html", 'r') as file:
        return file.read()

def handle_request(request):
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
    status_message = {200: "OK", 404: "Not Found"}.get(status_code, "OK")
    response = f"HTTP/1.1 {status_code} {status_message}\r\n"
    response += "Content-Type: text/html; charset=UTF-8\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    response += "\r\n"
    response += body
    return response

def run_server():
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(('127.0.0.1', 8058))
    socket_server.listen(5)

    while True:
        client_socket, addr = socket_server.accept()
        print(f"Подключение ... {addr}")

        request = client_socket.recv(1024).decode('utf-8')
        if request:
            response = handle_request(request)
            client_socket.sendall(response.encode('utf-8'))

        client_socket.close()

if __name__ == "__main__":
    run_server()
