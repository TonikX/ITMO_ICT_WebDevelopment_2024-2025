from dataclasses import dataclass


@dataclass
class Request:
    path: str
    method: str
    headers: dict[str, str]
    body: str
