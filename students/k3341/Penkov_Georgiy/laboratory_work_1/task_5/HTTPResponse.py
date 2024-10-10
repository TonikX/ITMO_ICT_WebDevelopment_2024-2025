class HTTPResponse:
    def __init__(self, status, status_text, headers=None, body=None):
        self.status = status
        self.status_text = status_text
        self.headers = headers
        self.body: str | None = body
        self.version = "HTTP/1.1"

    def get_response_str(self) -> str:
        response = ""
        status_line = f"{self.version} {self.status} {self.status_text}\r\n"
        response += status_line

        if self.headers:
            for key, value in self.headers:
                header_line = f"{key}: {value}\r\n"
                response += header_line
        else:
            headers = "Content-Type: text/html; charset=utf-8\r\n"
            headers += (
                f"Content-Length: {len(self.body.encode()) if self.body else 0}\r\n"
            )
            response += headers
        response += "\r\n"

        if self.body:
            response += self.body

        return response
