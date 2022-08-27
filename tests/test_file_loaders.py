import os.path
import unittest

from terravacuum import load_file, save_to_file, PluginLoader


class TestFileLoaders(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        PluginLoader.load_plugin('terravacuum.core_plugins.json_loader')
        PluginLoader.load_plugin('terravacuum.core_plugins.yaml_loader')

    def test_load_but_no_loader(self):
        data = load_file('file.unknown_extension')
        self.assertIsNone(data)

    def test_load_json(self):
        data = load_file('data_tests/test_plugin_json_loader.json')
        self.assertEqual(data['Author'], 'Robin LIORET')

    def test_load_yaml(self):
        data = load_file('data_tests/test_plugin_yml_loader.yml')
        self.assertEqual(data['Author'], 'Robin LIORET')

    def test_save_but_no_loader(self):
        result = save_to_file('file.unknown_extension', {})
        self.assertFalse(result)
        self.assertFalse(os.path.exists('file.unknown_extension'))

    def test_save_json(self):
        data1 = {'Name': 'Spock', 'Role': 'Commander'}
        result = save_to_file('data_tests/test_save_file.json', data1)
        self.assertTrue(result)
        self.assertTrue(os.path.isfile('data_tests/test_save_file.json'))
        data2 = load_file('data_tests/test_save_file.json')
        self.assertEqual(data2, data1)

    def test_save_yaml(self):
        data1 = {'Name': 'Spock', 'Role': 'Commander'}
        result = save_to_file('data_tests/test_save_file.yml', data1)
        self.assertTrue(result)
        self.assertTrue(os.path.isfile('data_tests/test_save_file.yml'))
        data2 = load_file('data_tests/test_save_file.yml')
        self.assertEqual(data2, data1)
