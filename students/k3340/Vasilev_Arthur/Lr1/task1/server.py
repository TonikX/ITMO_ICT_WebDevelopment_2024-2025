import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    server_address = ('localhost', 8081)
    
    server_socket.bind(server_address)
    
    print("Сервер запущен и слушает на localhost:12345")
    print("Ожидание сообщения от клиента...")
    
    try:
        while True:
            data, client_address = server_socket.recvfrom(1024)
            
            message = data.decode('utf-8')
            print(f"Получено от {client_address}: {message}")
            
            if message.lower() == 'exit':
                response = "Сервер завершает работу"
                server_socket.sendto(response.encode('utf-8'), client_address)
                print("Завершение работы сервера по запросу клиента")
                break
            
            response = "Hello, client"
            
            server_socket.sendto(response.encode('utf-8'), client_address)
            print(f"Отправлен ответ клиенту: {response}")
            
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    finally:
        server_socket.close()
        print("Сокет сервера закрыт")

if __name__ == "__main__":
    start_server()