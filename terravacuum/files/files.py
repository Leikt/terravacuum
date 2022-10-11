import logging
import os
from contextlib import contextmanager
from typing import Protocol, Optional, Any

from ..plugin_system import PluginLoader


class PFileLoader(Protocol):
    """Specific file type loader."""

    @staticmethod
    def load_file(filename: str) -> Optional[Any]:
        """Load data from the file. If the loader is not able to load the data. It returns None."""

    @staticmethod
    def save(filename: str, data: Any) -> bool:
        """Try to save the data and return its ability to save the file."""


def load_file(filename: str) -> Optional[Any]:
    """Use the file loaders plugins to load the file. Return None if no plugin can handle the extension"""
    for _, loader in PluginLoader.get('file_loader'):
        result = loader.load_file(filename)
        if result is not None:
            return result
    logging.warning('No plugin is able to load {}'.format(filename))
    return None


def save_to_file(filename: str, data: Any) -> bool:
    """Use the file loaders plugins to save data to the file. Return False if no plugin can handle the extension"""
    create_dir(filename)
    for _, loader in PluginLoader.get('file_loader'):
        if loader.save(filename, data):
            return True
    logging.warning('No plugin is able to save data to {}'.format(filename))
    return False


@contextmanager
def change_working_directory(path: str):
    """Execute code within another working directory."""
    old_dir = os.getcwd()
    os.makedirs(path, exist_ok=True)
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


def create_dir(filename: str):
    """Create directory if it doesn't exist."""
    basedir = os.path.dirname(filename)
    if basedir == '':
        return
    if os.path.isdir(basedir):
        return

    os.makedirs(basedir, exist_ok=True)
