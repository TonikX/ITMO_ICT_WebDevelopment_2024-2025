import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5555)
server_socket.bind(server_address)


server_socket.listen(1)
print("Server is waiting for a client...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connected client with the address: {client_address}")

    try:
        with open("index.html", "r") as file:
            html_content = file.read()
        http_response = f"HTTP/1.1 200 OK\nContent-Length: {len(html_content)}\n\n{html_content}"
        client_socket.send(http_response.encode('utf-8'))

    except Exception as e:
        print(f"Error while calculating the response: {e}")

    finally:
        client_socket.close()