from typing import Dict, Optional


class StudentRequest:
    def __init__(self,
                 method: str,
                 addr: str,
                 version_proto: str,
                 headers: Optional[Dict[str, str]] = None,
                 body: str = '') -> None:
        self.method = method
        self.addr = addr
        self.version_proto = version_proto
        self.headers = headers or {}
        self.body = body
