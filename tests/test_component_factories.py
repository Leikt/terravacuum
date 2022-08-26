import unittest

from mock_factories import MockComponent
from terravacuum import register_plugin_sockets, PluginLoader, get_component_factory, \
    WrongArgumentForComponentConstructor


class TestComponentFactories(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        PluginLoader.load_plugin('mock_factories')

    def test_mock_factory(self):
        factory = get_component_factory('mock')
        component = factory({'first_name': 'Leikt', 'name': 'SolReihin'})
        self.assertIsInstance(component, MockComponent)
        self.assertEqual('Leikt', component.first_name)
        self.assertEqual('SolReihin', component.name)

    def test_mock_raises(self):
        factory = get_component_factory('mock')
        with self.assertRaises(WrongArgumentForComponentConstructor):
            factory(None)
            factory([])
            factory("")
