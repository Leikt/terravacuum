import unittest

from mock_renderer import MockRenderer
from terravacuum import register_plugin_sockets, register_core_plugins, PluginLoader, get_renderer_factory


class TestRendererFactories(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        register_core_plugins()
        PluginLoader.load_plugin('mock_factories')
        PluginLoader.load_plugin('mock_renderer')

    def test_mock_root_factory(self):
        factory = get_renderer_factory('mock')
        root_renderer = factory()
        self.assertIsInstance(root_renderer, MockRenderer)
