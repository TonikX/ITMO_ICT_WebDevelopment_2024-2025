from socket import *
import os

# 获取当前文件所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, 'index.html')

# 确保 HTML 文件存在
if not os.path.exists(html_file_path):
    raise FileNotFoundError(f"HTML file not found at: {html_file_path}")

# 创建服务器套接字
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localhost', 9090))
server_socket.listen(1)

print("Server is running...")
print("http://localhost:9090")

while True:
    connection, client_address = server_socket.accept()
    try:
        print(f"Client: {client_address} is now in session.")

        # 接收客户端请求
        request = connection.recv(1024).decode()
        print(f"Client request: \n{request}")

        # 读取 HTML 文件内容
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # 创建 HTTP 响应
        response = f"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(html_content)}

{html_content}"""

        # 发送响应
        connection.sendall(response.encode())
        print("Response is sent to a client.")
    finally:
        connection.close()
        print(f"Connection with client {client_address} is closed.")
