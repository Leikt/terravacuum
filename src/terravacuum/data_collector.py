from typing import Protocol, Optional, Any

from .plugin_system import PluginLoader, PluginItemNotFoundError


class DataCollectorNotFoundError(PluginItemNotFoundError):
    """Exception raised when a data collector is requested but not found."""


class PDataCollector(Protocol):
    """Specific data collector."""

    @staticmethod
    def collect() -> Optional[Any]:
        """Collect the data and return it"""


def collect_data(key: str) -> Optional[Any]:
    """Collect the data from the given source. A plugin must be registered to this source."""
    return PluginLoader.get('data_collector')[key].collect()
