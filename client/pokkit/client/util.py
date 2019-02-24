import urllib.parse


def sanitize_fname(name: str) -> str:
    return urllib.parse.encode(name)
