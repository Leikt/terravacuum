from dataclasses import dataclass

from terravacuum import PluginLoader, PluginItemNotFoundError


@dataclass
class Mock:
    value: int = 0


class MockNotFoundError(PluginItemNotFoundError):
    pass


def register_plugin_sockets():
    PluginLoader.register_plugin_socket('mock_socket', 'register_mock', MockNotFoundError)


def register_mock() -> tuple[str, Mock]:
    yield '12', Mock(12)
    yield '52', Mock(52)
    yield '366', Mock(366)
