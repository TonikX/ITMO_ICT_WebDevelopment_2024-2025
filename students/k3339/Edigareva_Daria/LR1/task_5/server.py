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

    # Split the request into lines
    lines = request_data.split('\r\n')
    request_line = lines[0]
    method, path, protocol = request_line.split()

    if method == 'GET':
        # Load the main page template
        main_page = read_template('templates/main.html')

        # Generate the list of grades
        if subject_grades:
            grades_html = ''.join(f'<li>{subject}: {grade}</li>' for subject, grade in subject_grades.items())
        else:
            grades_html = '<p>No grades recorded.</p>'

        # Insert the grades list into the template
        response_body = main_page.replace('{{grades}}', grades_html)

        # Send the HTTP response
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + response_body
        client_connection.sendall(response.encode())

    elif method == 'POST':
        try:
            # Find the index of the blank line separating headers and body
            blank_line_index = lines.index('')
        except ValueError:
            client_connection.close()
            return

        headers = lines[1:blank_line_index]
        body = '\r\n'.join(lines[blank_line_index + 1:])

        # Extract the Content-Length header to determine the body size
        content_length = 0
        for header in headers:
            if header.lower().startswith('content-length'):
                content_length = int(header.split(':')[1].strip())
                break

        # Read the remaining body if it's incomplete
        while len(body.encode()) < content_length:
            body += client_connection.recv(1024).decode()

        # Parse the form data from the body
        form_data = urllib.parse.parse_qs(body)

        # Retrieve subject and grade from the form data
        subject = form_data.get('subject', [''])[0]
        grade = form_data.get('grade', [''])[0]

        # Store the data if both fields are provided
        if subject and grade:
            subject_grades[subject] = grade

        # Load the confirmation page template
        confirmation_page = read_template('templates/confirmation.html')

        # Insert the subject and grade into the template
        response_body = confirmation_page.replace('{{subject}}', subject).replace('{{grade}}', grade)

        # Send the HTTP response
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + response_body
        client_connection.sendall(response.encode())

    else:
        # Respond with 405 Method Not Allowed for unsupported methods
        response = 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
        client_connection.sendall(response.encode())

    client_connection.close()


def start_server():
    host = ''
    port = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f'Server is running on port {port}...')

        while True:
            client_conn, client_addr = server_socket.accept()
            process_request(client_conn)


if __name__ == '__main__':
    # Ensure the templates directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print('Templates directory created. Please add the HTML templates.')
    else:
        start_server()
