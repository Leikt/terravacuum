import unittest

from terravacuum_core import PluginLoader, register_plugin_sockets, load_file


class TestFileLoaders(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        PluginLoader.load_plugin('plugins.json_loader')
        PluginLoader.load_plugin('plugins.yaml_loader')

    def test_no_loader(self):
        data = load_file('file.unknown_extension')
        self.assertIsNone(data)

    def test_json(self):
        data = load_file('data_tests/test_plugin_json_loader.json')
        self.assertEqual(data['Author'], 'Robin LIORET')

    def test_yaml(self):
        data = load_file('data_tests/test_plugin_yml_loader.yml')
        self.assertEqual(data['Author'], 'Robin LIORET')
