import socket
from HTTPRequest import HTTPRequest
from HTTPResponse import HTTPResponse
from Course import Course
from CourseRepository import CourseRepository


"""
GET /courses/
POST /courses?name=&grade=
"""


class HTTPServer:
    def __init__(self, host="localhost", port=1234):
        self._host = host
        self._port = port
        self._course_repo = CourseRepository()

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((self._host, self._port))
            server_socket.listen()
            print(f"Listening on {self._host}:{self._port}")

            while True:
                client_socket, client_address = server_socket.accept()
                try:
                    self.serve_client(client_socket)
                except Exception as e:
                    print("Client serving failed: ", e)
        finally:
            server_socket.close()

    def serve_client(self, client_socket: socket.socket):
        try:
            data = self.recvall(client_socket)
            print(f"Received:\n{data}")
            request = HTTPRequest(data)
            response = self.handle_request(request)
            self.send_response(client_socket, response)
        except Exception as e:
            self.send_error(client_socket, e)
        finally:
            client_socket.close()

    def recvall(self, client_socket: socket.socket):
        data = b""
        while True:
            chunk = client_socket.recv(4096)
            data += chunk
            if not chunk:
                break
            if b"\r\n\r\n" in data:
                break
        return data.decode()

    def handle_request(self, request: HTTPRequest):
        match request.path:
            case "/courses":
                match request.method:
                    case "GET":
                        courses = self._course_repo.get_courses()
                        body = self.get_html_courses(courses)
                        headers = [
                            (
                                "Content-Type",
                                "text/html; charset=utf-8",
                            ),
                            ("Content-Length", len(body)),
                        ]
                        return HTTPResponse(200, "OK", headers, body)
                    case "POST":
                        if request.query_params is None:
                            raise ValueError("No query parameters provided")
                        self._course_repo.insert_course(
                            request.query_params["name"],
                            int(request.query_params["grade"]),
                        )
                        return HTTPResponse(201, "Created")
            case _:
                return HTTPResponse(400, "Bad Request")

    def send_response(
        self, client_socket: socket.socket, response: HTTPResponse
    ):
        response_str = response.get_response_str()
        client_socket.sendall(response_str.encode())
        print(f"Sent:\n{response_str}")

    def send_error(self, client_socket: socket.socket, err: Exception):
        status = 500
        status_text = "Internal Server Error"
        body = str(err)
        print(f"Error: {body}")
        response = HTTPResponse(status, status_text, body=body)
        self.send_response(client_socket, response)

    def get_html_courses(self, courses: list[Course]):
        html = "<html><head><title>Courses</title></head><body>"

        html += "<h1>Courses</h1>"
        if courses:
            html += "<ul>"
            for course in courses:
                html += f"<li>ID: {course.id}, Name: {course.name},\
                  Grade: {course.grade}</li>"
            html += "</ul>"
        else:
            html += "<p>No courses available.</p>"
        html += "</body></html>"
        return html


if __name__ == "__main__":
    host = "localhost"
    port = 1234
    server = HTTPServer(host, port)
    server.run()
