import hashlib


def get_string_hash(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()
