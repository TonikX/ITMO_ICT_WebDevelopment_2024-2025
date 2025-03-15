import socket
import signal


def raise_timeout(signum, frame):
    """
    Функция для рейза ошибки таймаута
    :param signum:
    :param frame:
    :return:
    """
    raise TimeoutError


def load_html():
    """
    gets HTML file from disk
    :return: readed file
    """
    with open(
            "/Users/alexr/Documents/study/sem5/web_prog/ITMO_ICT_WebDevelopment_2024-2025/students/k3342/Rozanov_Alexey/lab_1/task_3/index.html",
            "r") as file:
        return file.read()


def start_server(host='127.0.0.1', port=8088):
    """
    server works - start, connect client and return page
    :param host: OPTIONAL hostname of the server
    :param port: OPTIONAL port of the server
    :return:
    """
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    socket_server.bind((host, port))

    socket_server.listen(5)
    print(f"Server running on {host}:{port}")

    while True:
        client_connection, client_address = socket_server.accept()
        print(f"Client {client_address}")

        request = client_connection.recv(1024).decode()
        print(f"Client requested: {request}")

        html_content = load_html()

        response = ("HTTP/1.1 200 OK\r\n" "Content-Type: text/html;\r\n" "Content-Length: {}\r\n"
                    .format(len(html_content)) + "\r\n" + html_content)

        client_connection.sendall(response.encode())
        client_connection.close()


if __name__ == "__main__":

    signal.signal(signal.SIGALRM, raise_timeout)
    signal.alarm(60)

    try:
        start_server()
    finally:
        signal.alarm(0)
