import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


HOST = (socket.gethostname(), 8000)


server_socket.bind(HOST)


server_socket.listen(1)

print("Сервер ожидает подключения...")

while True:

    conn, addr = server_socket.accept()
    print(f"Подключение установлено с {addr}")

    try:

        with open("index.html", "r") as index_html:
            text = index_html.read()


        response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + text


        conn.sendall(response.encode("utf-8"))
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:

        conn.close()
