class HTTPRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.path = None
        self.query_params: dict[str, any] | None = None
        self.version = "HTTP/1.1"
        self.headers: dict[str, str] = dict()
        self.body: str | None = None

        self.parse(data)

    def parse(self, data: str):
        lines = data.splitlines()
        request_line = lines[0]
        words = request_line.split()
        if len(words) != 3:
            raise Exception("Malformed request line")

        self.method, self.uri, self.version = words
        self.parse_uri()

        if self.version != "HTTP/1.1":
            raise Exception("Unexpected HTTP version")

        for line in lines[1:]:
            if line.strip() == "":
                break
            key, value = line.split(":", 1)
            self.headers[key.strip()] = value.strip()

        body_start_index = lines.index("") + 1
        self.body = "\n".join(lines[body_start_index:])

    def parse_uri(self):
        if "?" in self.uri:
            self.path, query = self.uri.split("?", 1)
            self.parse_query(query)
        else:
            self.path = self.uri

    def parse_query(self, query: str):
        if not query:
            self.query_params = None
            return
        self.query_params = dict()
        for param in query.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                self.query_params[key] = value
            else:
                self.query_params[param] = None
