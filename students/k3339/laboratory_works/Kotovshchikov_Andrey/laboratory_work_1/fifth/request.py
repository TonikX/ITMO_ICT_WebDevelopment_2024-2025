from dataclasses import dataclass
from io import BufferedReader
from urllib.parse import parse_qs, urlparse


@dataclass(kw_only=True, slots=True)
class Request:
    method: str
    url: str
    version: str
    headers: dict[str, str]
    stream: BufferedReader

    @property
    def path(self):
        parsed_url = self._parse_url()
        return parsed_url.path

    @property
    def query(self):
        parsed_url = self._parse_url()
        return parse_qs(parsed_url.query)

    def _parse_url(self):
        return urlparse(self.url)
