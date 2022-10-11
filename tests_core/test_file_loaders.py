import os.path
import unittest

from terravacuum import register_plugin_sockets
from terravacuum.plugin_system import PluginLoader
from terravacuum.files import load_file, save_to_file, change_working_directory


class TestFileLoaders(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        PluginLoader.load_plugin('terravacuum.core_plugins.json_loader')
        PluginLoader.load_plugin('terravacuum.core_plugins.yaml_loader')
        PluginLoader.load_plugin('terravacuum.core_plugins.terraform_loader')

    def test_load_but_no_loader(self):
        data = load_file('file.unknown_extension')
        self.assertIsNone(data)

    def test_load_json(self):
        data = load_file('data_tests/test_plugin_json_loader.json')
        self.assertEqual(data['Author'], 'Robin LIORET')

    def test_load_tf(self):
        data = load_file('data_tests/test_plugin_tf_loader.tf')
        self.assertEqual('LOADED', data)

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

    def test_save_tf(self):
        data1 = 'SAVED'
        result = save_to_file('data_tests/test_save_file.tf', data1)
        self.assertTrue(result)
        self.assertTrue(os.path.isfile('data_tests/test_save_file.tf'))
        data2 = load_file('data_tests/test_save_file.tf')
        self.assertEqual(data2, data1)

    def test_other_dir(self):
        cur_dir = os.getcwd()
        self.assertEqual(os.getcwd(), cur_dir)
        with change_working_directory('data_tests/'):
            self.assertNotEqual(cur_dir, os.getcwd())

        with change_working_directory('data_tests/dummy/dummy/'):
            self.assertTrue(os.path.exists('existing_file'))
