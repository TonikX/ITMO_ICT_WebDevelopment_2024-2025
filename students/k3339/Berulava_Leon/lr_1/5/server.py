import socket
import urllib.parse


def client_processing(client):
    request = client.recv(1024).decode()
    temp = request.split('\r\n')
    method = temp[0].split(' ')[0]
    url = temp[0].split(' ')[1]
    if method == 'GET':
        html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Marks book</title>
            </head>
            <body>
                <h3>Welcome to our marks book!</h3>

                <h4>Enter new grades:</h4>
                <form method="POST" action="/">
                    Enter the subject: <input type="text" name="subject" /> <br/>
                    Enter the mark: <input type="text" name="mark" /> <br/>
                    <input type="submit" value="Add mark">
                </form>

                <h4>All grades:</h4>
                <style type="text/css">
                BODY {
                background: white; 
                }
                TABLE {
                width: 300px; 
                border-collapse: collapse; 
                border: 2px solid white; 
                }
                TD, TH {
                padding: 3px; 
                border: 1px solid black; 
                text-align: left; 
                }
                </style>
                <table>
                    <tr><th>The subject</th><th>The mark</th></tr>\r\n"""

        for key in subjects_grades.keys():
            html_content = html_content + '<tr><td>' + str(key) + '</td><td>' + ' '.join(
                map(str, subjects_grades[key])) + '</td></tr>\r\n'

        html_content = html_content + '</table>\r\n' + '</body>\r\n' + '</html>\r\n'

        http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=ASCII\r\n"
                f"Content-Length: {len(html_content)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                + html_content
        )

    elif method == 'POST':
        info = temp[-1]
        parsed_info = urllib.parse.parse_qs(info)
        subject = parsed_info.get('subject', [''])[0]
        mark = parsed_info.get('mark', [''])[0]

        if subject in subjects_grades.keys():
            subjects_grades[subject].append(mark)
        else:
            subjects_grades[subject] = [mark]
        print("subjects_grades: ", subjects_grades)

        html_content = '''
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Marks book</title>
            </head>
            <body>
                <h3>Welcome to our marks book!</h3>
                <h4>Mark is saved!</h4>
        '''
        http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=ASCII\r\n"
                f"Content-Length: {len(html_content)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                + html_content
        )

    client.sendall(http_response.encode())
    client.close()


subjects_grades = {}

HOST = 'localhost'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"HTTP is running on {HOST}:{PORT}...")

while True:
    client, client_address = server_socket.accept()
    print(f'Connection from {client_address}')
    client_processing(client)