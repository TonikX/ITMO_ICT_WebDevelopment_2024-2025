import socket
import os

grades = {}

def handle_request(request):

    global grades
    lines = request.splitlines()
    request_line = lines[0].split()

    if request_line[0] == 'POST':
        if len(lines) > 1:
            data = lines[-1].split('&')
            discipline = data[0].split('=')[1] if len(data) > 0 else "unknown"
            grade = data[1].split('=')[1] if len(data) > 1 else "unknown"

            if discipline not in grades:
                grades[discipline] = []
            grades[discipline].append(grade)

            update_html_file()
            print(f"Added: {discipline} - {grade}")
            return "HTTP/1.1 200 OK\r\n\r\nData updated."
        else:
            return "HTTP/1.1 400 Bad Request\r\n\r\nNo data."

    elif request_line[0] == 'GET':
        return serve_html_file()

    return "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed."


def update_html_file():

    with open("grades.html", "w", encoding='utf-8') as f:
        f.write("<html><head><meta charset='UTF-8'></head><body>")
        f.write("<h1>Grades</h1>")
        f.write("<table border='1'>")
        f.write("<tr><th>Discipline</th><th>Grades</th></tr>")
        for discipline, grade_list in grades.items():
            grades_str = ", ".join(grade_list)
            f.write(f"<tr><td>{discipline}</td><td>{grades_str}</td></tr>")
        f.write("</table></body></html>")
    print("HTML-file updated.")


def serve_html_file():

    if os.path.exists("grades.html"):
        with open("grades.html", "r", encoding='utf-8') as f:
            content = f.read()
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{content}"
    else:
        return "HTTP/1.1 404 Not Found\r\n\r\nGrades file not found."


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8080))
    server.listen(4)
    print("Server started: http://localhost:8080")

    while True:
        try:
            client, addr = server.accept()
            print(f"Connection from {addr}")
            request = client.recv(1024).decode('utf-8')
            if request:
                print(f"Request: {request}")
                response = handle_request(request)
                client.sendall(response.encode('utf-8'))
            client.close()
        except Exception as e:
            print(f"Error: {e}")


start_server()