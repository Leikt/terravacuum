import logging
from typing import Protocol, Optional, Any


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


class DataCollectorPluginSocket:
    """Plugin socket for the file loading."""

    __plugins: dict[str, PDataCollector] = {}

    @classmethod
    def register(cls, module):
        if not hasattr(module, 'register_data_collectors'):
            return
        for source, plugin in module.register_data_collectors():
            if plugin in cls.__plugins.values():
                continue
            if source in cls.__plugins:
                logging.warning('A data collector is already registered on source "{}"'.format(source))
                continue

            cls.__plugins[source] = plugin

    @classmethod
    def get_plugin(cls, source: str) -> PDataCollector:
        if source not in cls.__plugins:
            raise DataCollectorNotFoundError(source)
        return cls.__plugins[source]


def collect_data(source: str) -> Optional[Any]:
    """Collect the data from the given source. A plugin must be registered to this source."""
    return DataCollectorPluginSocket.get_plugin(source).collect()
