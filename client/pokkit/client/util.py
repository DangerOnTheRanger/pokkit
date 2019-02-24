import io
import urllib.parse


def sanitize_fname(name: str) -> str:
    return urllib.parse.encode(name)


def open_or_default(fname, default=''):
    try:
        return open(fname, 'r')
    except FileNotFoundError:
        return io.StringIO(default)
