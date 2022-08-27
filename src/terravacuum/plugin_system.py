import importlib
import logging
from typing import Protocol


class PPluginSocket(Protocol):
    """Common interface for the services that use plugins."""

    @classmethod
    def register(cls, module):
        """Register a plugin from the given module"""


class PluginLoader:
    """Loads and register the plugins."""
    _known_sockets: list[PPluginSocket] = []

    @classmethod
    def register_plugin_socket(cls, obj: PPluginSocket):
        """Add the object to the list of objects that can register plugins."""
        if obj in cls._known_sockets:
            return

        cls._known_sockets.append(obj)
        logging.debug('Plug socket {} registered.'.format(obj.__class__.__name__))

    @classmethod
    def register_plugin(cls, module):
        """Register plugin to the program."""
        for plugin_user in cls._known_sockets:
            try:
                plugin_user.register(module)
            except AttributeError:
                continue

    @staticmethod
    def load_plugin(name: str):
        try:
            module = importlib.import_module(name)
            PluginLoader.register_plugin(module)
            logging.debug('Plugin loaded: {}'.format(name))
        except ModuleNotFoundError:
            logging.error('Plugin not found: {}'.format(name))

    @staticmethod
    def load_plugins_from_file(filename: str):
        with open(filename, 'r') as file:
            plugin_names = file.read().splitlines()
        for plugin_name in plugin_names:
            PluginLoader.load_plugin(plugin_name)


def register_plugin_socket(cls):
    """Register the class as a plugin socket."""
    PluginLoader.register_plugin_socket(cls)
    return cls
