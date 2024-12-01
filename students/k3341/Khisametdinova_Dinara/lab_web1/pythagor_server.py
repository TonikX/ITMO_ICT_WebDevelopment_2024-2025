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
