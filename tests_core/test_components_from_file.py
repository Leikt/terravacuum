import unittest

from mock_factories import MockComponent
from terravacuum import PluginLoader, load_file, create_component, create_component_context


class TestComponentsFromFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        PluginLoader.load_plugin('mock_factories')

    def test_load_simple_component(self):
        context = create_component_context()
        data = load_file('data_tests/test_component.yml')
        component = create_component(context, data)
        self.assertIsInstance(component, MockComponent)
        self.assertEqual('MIETTAUX', component.name)
        self.assertEqual('George', component.first_name)
