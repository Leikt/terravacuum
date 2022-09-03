import unittest

from terravacuum.plugin_system import PluginLoader


class TestPluginSystem(unittest.TestCase):
    def test_mock_plugin(self):
        PluginLoader.load_plugin('mock_plugin')

    def test_load_from_file(self):
        PluginLoader.load_plugins_from_file('data_tests/mock_plugins.txt')
        self.assertGreater(len(list(PluginLoader.get('mock_socket'))), 0)
