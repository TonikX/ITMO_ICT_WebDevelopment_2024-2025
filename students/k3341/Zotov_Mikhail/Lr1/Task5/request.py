from functools import lru_cache
from urllib.parse import urlparse, parse_qs


class Request:
    def __init__(self, method: str, target: str, version: str, headers: dict, body: str):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.body = body

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
