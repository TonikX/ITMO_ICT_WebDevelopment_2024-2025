from server import Server

class EchoServer(Server):
    def handle_echo(self):
        data, client = self.handle_client() 
        print(f"Received: {data}")
        response = "Hello, UDP client"  
        self.send_response(response, client) 

if __name__ == "__main__":
    server = EchoServer(protocol_type="UDP")
    server.handle_echo()
    server.close()
