import unittest

from mock_plugin import MockSocket
from terravacuum_core import PluginLoader


class TestPluginSystem(unittest.TestCase):
    def test_mock_plugin(self):
        PluginLoader.register_plugin_socket(MockSocket)
        PluginLoader.load_plugin('mock_plugin')
        self.assertGreater(len(list(MockSocket.each())), 0)

    def test_load_from_file(self):
        PluginLoader.register_plugin_socket(MockSocket)
        PluginLoader.load_plugins_from_file('data_tests/mock_plugins.txt')
        self.assertGreater(len(list(MockSocket.each())), 0)
