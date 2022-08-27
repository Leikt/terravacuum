import logging
from typing import Protocol, Optional, Any

from .plugin_system import register_plugin_socket, plugin_registerer


class DataCollectorNotFoundError(Exception):
    """Exception raised when a data collector is requested but not found."""

    def __init__(self, source: str):
        self.source = source
        self.message = 'Data collector "{}" was not found.'.format(source)
        super().__init__(self.message)


class PDataCollector(Protocol):
    """Specific data collector."""

    @staticmethod
    def collect() -> Optional[Any]:
        """Collect the data and return it"""


@register_plugin_socket
class DataCollectorPluginSocket:
    """Plugin socket for the data collectors."""

    __plugins: dict[str, PDataCollector] = {}

    @classmethod
    @plugin_registerer('register_data_collectors')
    def register(cls, element):
        source, plugin = element
        if source in cls.__plugins:
            logging.warning('A data collector is already registered on source "{}"'.format(source))
            return

        cls.__plugins[source] = plugin

    @classmethod
    def get_plugin(cls, source: str) -> PDataCollector:
        if source not in cls.__plugins:
            raise DataCollectorNotFoundError(source)
        return cls.__plugins[source]


def collect_data(source: str) -> Optional[Any]:
    """Collect the data from the given source. A plugin must be registered to this source."""
    return DataCollectorPluginSocket.get_plugin(source).collect()
