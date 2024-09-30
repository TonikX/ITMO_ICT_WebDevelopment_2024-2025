class HTTPResponse:
    def __init__(self, status, status_text, headers=None, body=None):
        self.status = status
        self.status_text = status_text
        self.headers = headers
        self.body = body
        self.version = "HTTP/1.1"

    def get_response_str(self) -> str:
        response = ""
        status_line = f"{self.version} {self.status} {self.status_text}\r\n"
        response += status_line

        if self.headers:
            for key, value in self.headers:
                header_line = f"{key}: {value}\r\n"
                response += header_line
        response += "\r\n"

        if self.body:
            response += self.body

        return response
