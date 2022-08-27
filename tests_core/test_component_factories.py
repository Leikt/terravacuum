import unittest

from mock_factories import MockComponent, MockParentComponent, MockWithChildrenComponent
from terravacuum import PluginLoader, get_component_factory, \
    WrongArgumentForComponentConstructor, ComponentFactoryNotFound, WrongDataTypeError, MissingChildrenDataError, \
    TooManyChildComponents, WrongInlineArgument


class TestComponentFactories(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
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

    def test_auto_children(self):
        data = {
            'children': [
                {'mock': {'name': 'A', 'first_name': 'AA'}},
                {'mock': {'name': 'B', 'first_name': 'BB'}}
            ]
        }
        factory = get_component_factory('mock_auto_children')
        component = factory(data)
        self.assertIsInstance(component, MockWithChildrenComponent)
        self.assertEqual(2, len(component.children))
        self.assertIsInstance(component.children[0], MockComponent)

    def test_auto_children_raises(self):
        factory = get_component_factory('mock_auto_children')
        with self.assertRaises(WrongDataTypeError):
            factory(None)
            factory({'children': 'wrong_type'})
        with self.assertRaises(MissingChildrenDataError):
            factory({})
        with self.assertRaises(TooManyChildComponents):
            factory({
                'children': [
                    {'mock1': {}, 'too_much': {}}
                ]
            })

    def test_inline_dict(self):
        factory = get_component_factory('mock_with_inline_arguments')
        component = factory('name=MIETTAUX first_name=George')
        self.assertIsInstance(component, MockComponent)
        self.assertEqual('George', component.first_name)
        self.assertEqual('MIETTAUX', component.name)

    def test_inline_single(self):
        factory = get_component_factory('mock_with_inline_arguments')
        component = factory('George MIETTAUX')
        self.assertIsInstance(component, MockComponent)
        self.assertEqual('George', component.first_name)
        self.assertEqual('MIETTAUX', component.name)

    def test_inline_error(self):
        factory = get_component_factory('mock_with_inline_dict')
        with self.assertRaises(WrongInlineArgument):
            factory('George MIETTAUX')
