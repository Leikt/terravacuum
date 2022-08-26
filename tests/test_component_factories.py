import unittest

from mock_factories import MockComponent, MockParentComponent
from terravacuum import register_plugin_sockets, PluginLoader, get_component_factory, \
    WrongArgumentForComponentConstructor, ComponentFactoryNotFound


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

    def test_factory_not_found(self):
        with self.assertRaises(ComponentFactoryNotFound):
            get_component_factory('not_registered')

    def test_parent_factory(self):
        data = {
            'destination': 'somewhere',
            'mock_child': {'name': 'A', 'first_name': 'AA'}
        }
        factory = get_component_factory('mocks')
        component = factory(data)
        self.assertIsInstance(component, MockParentComponent)
        self.assertEqual(data['destination'], component.destination)
        self.assertIsInstance(component.child, MockComponent)
        self.assertEqual('A', component.child.name)
        self.assertEqual('AA', component.child.first_name)

    def test_parent_factory_raises(self):
        data = {
            'destination': 'somewhere',
            'mock_child': {'name': 'A'}
        }
        factory = get_component_factory('mocks')
        with self.assertRaises(WrongArgumentForComponentConstructor):
            factory(data)
            factory(None)
            factory("")
            factory([])
