import importlib
import logging
from dataclasses import dataclass, field
from typing import Any


class PluginItemNotFoundError(Exception):
    """Exception raised when an item is not found in the socket."""

    def __init__(self, socket: str, item: str):
        self.item = item
        self.message = f'Item "{item}" not found in socket "{socket}"'
        super().__init__(self.message)


@dataclass
class PluginSocket:
    """Contains the loaded elements from a plugin."""
    __name: str
    __register_method: str
    __exception: type
    __items: dict[str, Any] = field(default_factory=dict)

    def register_plugin(self, module):
        """Register the plugin if it matches the socket requirements."""
        if not hasattr(module, self.__register_method):
            return

        for key, value in module.__getattribute__(self.__register_method)():
            if not self._check_registration(key):
                continue

            self.__items[key] = value

    def __getitem__(self, item) -> Any:
        if item not in self.__items:
            raise self.__exception(self.__name, item)
        return self.__items[item]

    def __iter__(self) -> tuple[str, Any]:
        for key, item in self.__items.items():
            yield key, item

    def _check_registration(self, key: str) -> bool:
        if key in self.__items:
            logging.warning('PluginSocket "{}": a item is already registered on "{}"'.format(self.__name, key))
            return False
        return True


class PluginLoader:
    """Loads and register the plugins."""
    __sockets: dict[str, PluginSocket] = {}

    @classmethod
    def register_plugin_socket(cls, name: str, register_method: str, exception: type = PluginItemNotFoundError):
        """Add the object to the list of objects that can register plugins."""
        cls.__sockets[name] = PluginSocket(name, register_method, exception)
        logging.debug('Plugin socket {} registered.'.format(name))

    @classmethod
    def register_plugin(cls, module):
        """Register plugin to the program."""
        for plugin_user in cls.__sockets.values():
            plugin_user.register_plugin(module)

    @classmethod
    def get(cls, socket_name: str) -> PluginSocket:
        return cls.__sockets[socket_name]

    @staticmethod
    def load_plugin(name: str):
        try:
            module = importlib.import_module(name)
            if hasattr(module, 'register_plugin_sockets'):
                module.__getattribute__('register_plugin_sockets')()
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
