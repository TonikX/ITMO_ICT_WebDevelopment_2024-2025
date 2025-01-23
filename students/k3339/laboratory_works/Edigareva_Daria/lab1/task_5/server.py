import socket
import urllib.parse
import os

subject_grades = {}

def read_template(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

def process_request(client_connection):
    request_data = client_connection.recv(1024).decode()
    if not request_data:
        client_connection.close()
        return

    lines = request_data.split('\r\n')
    request_line = lines[0]
    method, path, protocol = request_line.split()

    if method == 'GET':
        main_page = read_template('templates/main.html')

        if subject_grades:
            grades_html = ''.join(
                f'<li>{subject}: {", ".join(grades)}</li>'
                for subject, grades in subject_grades.items()
            )
        else:
            grades_html = '<p>No grades recorded.</p>'

        response_body = main_page.replace('{{grades}}', grades_html)

        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + response_body
        client_connection.sendall(response.encode())

    elif method == 'POST':
        try:
            blank_line_index = lines.index('')
        except ValueError:
            client_connection.close()
            return

        headers = lines[1:blank_line_index]
        body = '\r\n'.join(lines[blank_line_index + 1:])

        content_length = 0
        for header in headers:
            if header.lower().startswith('content-length'):
                content_length = int(header.split(':')[1].strip())
                break

        while len(body.encode()) < content_length:
            body += client_connection.recv(1024).decode()

        form_data = urllib.parse.parse_qs(body)

        subject = form_data.get('subject', [''])[0]
        grade = form_data.get('grade', [''])[0]

        if subject and grade:
            if subject in subject_grades:
                subject_grades[subject].append(grade)
            else:
                subject_grades[subject] = [grade]

        confirmation_page = read_template('templates/confirmation.html')

        response_body = confirmation_page.replace('{{subject}}', subject).replace('{{grade}}', grade)

        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + response_body
        client_connection.sendall(response.encode())

    else:
        response = 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
        client_connection.sendall(response.encode())

    client_connection.close()

def start_server():
    host = ''
    port = 8081
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f'Server is running on port {port}...')

        while True:
            client_conn, client_addr = server_socket.accept()
            process_request(client_conn)

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print('Templates directory created. Please add the HTML templates.')
    else:
        start_server()
