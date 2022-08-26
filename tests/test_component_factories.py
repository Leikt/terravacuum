import unittest

from mock_factories import MockComponent
from terravacuum import register_plugin_sockets, PluginLoader, create_component


class TestComponentFactories(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        PluginLoader.load_plugin('mock_factories')

    def test_mock_factory(self):
        component = create_component('mock', {'first_name': 'Leikt', 'name': 'SolReihin'})
        self.assertIsInstance(component, MockComponent)
        self.assertEqual('Leikt', component.first_name)
        self.assertEqual('SolReihin', component.name)

    def test_mock_raises(self):
        with self.assertRaises(TypeError):
            create_component('mock', None)
            create_component('mock', [])
            create_component('mock', "")
