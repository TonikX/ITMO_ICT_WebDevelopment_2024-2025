from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServerExeption(Exception):
    status_code: int
    reason: str
