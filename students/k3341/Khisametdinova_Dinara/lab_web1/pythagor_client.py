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
