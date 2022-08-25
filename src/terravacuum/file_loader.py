import logging
from typing import Protocol, Optional, Any


class PFileLoader(Protocol):
    """Specific file type loader."""

    @staticmethod
    def load_file(filename: str) -> Optional[Any]:
        """Load data from the file. If the loader is not able to load the data. It returns None."""

    @staticmethod
    def save(filename: str, data: Any) -> bool:
        """Try to save the data and return its ability to save the file."""


class FileLoaderPluginSocket:
    """Plugin socket for the file loading."""

    __plugins: list[PFileLoader] = []

    @classmethod
    def register(cls, module):
        if not hasattr(module, 'register_file_loaders'):
            return
        for plugin in module.register_file_loaders():
            if plugin in cls.__plugins:
                continue

            cls.__plugins.append(plugin)

    @classmethod
    def get_plugins(cls) -> list[PFileLoader]:
        return cls.__plugins


def load_file(filename: str) -> Optional[Any]:
    """Use the file loaders plugins to load the file. Return None if no plugin can handle the extension"""
    for plugin in FileLoaderPluginSocket.get_plugins():
        result = plugin.load_file(filename)
        if result is not None:
            return result
    logging.warning('No plugin is able to load {}'.format(filename))
    return None


def save_to_file(filename: str, data: Any) -> bool:
    """Use the file loaders plugins to save data to the file. Return False if no plugin can handle the extension"""
    for plugin in FileLoaderPluginSocket.get_plugins():
        if plugin.save(filename, data):
            return True
    logging.warning('No plugin is save data to {}'.format(filename))
    return False
