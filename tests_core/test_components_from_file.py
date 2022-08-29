import unittest

from mock_factories import MockComponent
from terravacuum import PluginLoader, load_file, create_component


class TestComponentsFromFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        PluginLoader.load_plugin('mock_factories')

    def test_load_simple_component(self):
        data = load_file('data_tests/test_component.yml')
        component = create_component(data)
        self.assertIsInstance(component, MockComponent)
        self.assertEqual('MIETTAUX', component.name)
        self.assertEqual('George', component.first_name)
