from dataclasses import dataclass, field


@dataclass(kw_only=True, slots=True)
class Response:
    status_code: int
    reason: str
    body: bytes | None = field(default=None)
    headers: dict[str, str] = field(default_factory=dict)
