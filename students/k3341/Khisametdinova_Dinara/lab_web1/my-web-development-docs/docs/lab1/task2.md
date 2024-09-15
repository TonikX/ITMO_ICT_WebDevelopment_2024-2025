# Task 2

   Реализовать клиентскую и серверную часть приложения. Клиент запрашивает у
сервера выполнение математической операции, параметры, которые вводятся с
клавиатуры. Сервер обрабатывает полученные данные и возвращает результат
клиенту. Варианты:

**a. Теорема Пифагора**

b. Решение квадратного уравнения.

c. Поиск площади трапеции.

d. Поиск площади параллелограмма.

Вариант выбирается в соответствии с порядковым номером в журнале. Пятый
студент получает вариант 1 и т.д.
Обязательно использовать библиотеку socket
Реализовать с помощью протокола TCP

pythagor_server.py
```python
import math
from server import Server

class PythagorasServer(Server):
    def handle_pythagoras_request(self):
        data, conn = self.handle_client()
        print(f"Received from client: {data}")

        a, b = map(float, data.split(","))
        c = math.sqrt(a**2 + b**2)
        result = str(c)

        self.send_response(result, conn)

if __name__ == "__main__":
    server = PythagorasServer(protocol_type="TCP")
    server.handle_pythagoras_request()
    server.close()
```
pythagor_client.py
```python
from client import Client

class PythagorasClient(Client):
    def send_data(self, a: float, b: float):
        data = f"{a},{b}"
        self.send_message(data)
        print(f"Sent to server: {data}")

    def receive_result(self) -> float:
        result = self.receive_response() 
        print(f"Received from server: {result}")
        return float(result)


if __name__ == "__main__":
    client = PythagorasClient(protocol_type="TCP")
    a = float(input("Введите длину первого катета: "))
    b = float(input("Введите длину второго катета: "))
    client.send_data(a, b)
    result = client.receive_result()
    print(f"Длина гипотенузы: {result}")
    client.close()
```
