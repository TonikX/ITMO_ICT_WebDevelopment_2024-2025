import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    server_address = ('localhost', 8081)
    
    print("Клиент запущен")
    print("Для выхода введите 'exit'")
    
    try:
        while True:
            message = input("Введите сообщение для сервера: ")
            
            client_socket.sendto(message.encode('utf-8'), server_address)
            
            if message.lower() == 'exit':
                print("Завершение работы клиента")
                break
            
            # Ждем ответ от сервера
            data, _ = client_socket.recvfrom(1024)
            response = data.decode('utf-8')
            
            print(f"Получен ответ от сервера: {response}")
            
    except KeyboardInterrupt:
        print("\nКлиент остановлен пользователем")
    except ConnectionRefusedError:
        print("Ошибка: Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    finally:
        # Всегда закрываем сокет
        client_socket.close()
        print("Сокет клиента закрыт")

# Запускаем клиент, только если файл запущен напрямую
if __name__ == "__main__":
    start_client()