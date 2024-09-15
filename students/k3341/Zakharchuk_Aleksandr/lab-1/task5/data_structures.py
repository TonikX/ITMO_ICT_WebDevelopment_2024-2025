import functools
import io
from urllib.parse import ParseResult, parse_qs, urlparse


class Request:
    def __init__(
            self,
            method: str,
            target: str,
            version: str,
            headers: dict[str, str],
            stream: io.BufferedReader,
        ):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.stream = stream

    def body(self) -> str:
        size = self.headers.get("Content-Length")
        if not size:
            return None
        return self.stream.read(int(size)).decode()

    @property
    def path(self) -> str:
        return self.url.path

    @property
    @functools.lru_cache(maxsize=None)
    def query(self) -> dict[str, str]:
        return parse_qs(self.url.query)

    @property
    @functools.lru_cache(maxsize=None)
    def url(self) -> ParseResult:
        return urlparse(self.target)


class Response:
    def __init__(
            self,
            status: str,
            reason: str,
            headers: dict[str, str] | None = None,
            body: str | None = None,
        ):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


class HTTPError(Exception):
  def __init__(self, status: str, reason: str, body: str | None = None):
    super()
    self.status = status
    self.reason = reason
    self.body = body
