import os

_current_dir: list[bytes] = []


def _set_current_dir(path: str) -> None:
    global _current_dir
    _current_dir = os.path.split(path)


def _get_current_dir():
    global _current_dir
    return _current_dir


def _get_current_dir_str() -> bytes:
    global _current_dir
    return os.path.join(*_current_dir)


def set_dir(path: str, create: bool = True) -> None:
    """Set the directory where the renderers will create files."""

    _set_current_dir(path)
    if create and not os.path.exists(_get_current_dir_str()):
        os.makedirs(_get_current_dir_str())


def get(path: str = '') -> str:
    """Build a path from the current directory and the given relative path."""

    path = os.path.split(path)
    final = os.path.join(*_get_current_dir(), *path)
    return final


def cd(path: str) -> None:
    """Change path location using a relative path."""

    path = os.path.split(path)
    path = os.path.join(*_get_current_dir(), *path)
    set(path)


def reset() -> None:
    """Reset the rpath to the working directory."""
    set_dir(os.getcwd(), False)


reset()
