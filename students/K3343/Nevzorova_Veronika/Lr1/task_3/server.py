import socket

def load_html():
    with open("/Users/veronikanevzorova/Desktop/web/ITMO_ICT_WebDevelopment_2024-2025/task_3/index.html", "r") as file:
        return file.read()

def start_server(host='127.0.0.1', port=8080):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    socket_server.bind((host, port))
    
    socket_server.listen(5)
    print(f"Сервер запущен на {host}:{port}")
    
    while True:
        client_connection, client_address = socket_server.accept()
        print(f"Подключение от {client_address}")
        
        request = client_connection.recv(1024).decode()
        print(f"Запрос от клиента: {request}")

        html_content = load_html()

        response = ("HTTP/1.1 200 OK\r\n" "Content-Type: text/html;\r\n" "Content-Length: {}\r\n".format(len(html_content)) + "\r\n" + html_content
        )
        client_connection.sendall(response.encode())
        client_connection.close()

if __name__=="__main__":
    start_server()
