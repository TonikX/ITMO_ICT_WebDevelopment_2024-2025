from functools import lru_cache
from urllib.parse import urlparse, parse_qs


class Request:
    def __init__(self, data):
        self.method, self.target, self.version = self.parse_request(data)
        self.headers = self.parse_headers(data)
        self.body = self.parse_body(data)

    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)

    @staticmethod
    def parse_request(data):
        line = ''
        i = 0
        while '\r\n' not in line:
            line += data[i]
            i += 1
        request_line = line.replace('\r\n', '').split()
        method = request_line[0]
        url = request_line[1]
        version = request_line[2]
        return method, url, version

    @staticmethod
    def parse_headers(data):
        headers = {}
        lines = data.split('\r\n')[1:-2]
        for line in lines:
            header, value = line.split(': ')
            headers[header] = value
        return headers

    @staticmethod
    def parse_body(data):
        body = data.split('\r\n\r\n')[1]
        return body
