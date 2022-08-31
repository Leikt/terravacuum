import unittest

from mock_factories import MockComponent, MockParentComponent
from mock_rendering import MockRendererNoExpression, MockRendererWithExpression, MockParentRenderer
from terravacuum import PluginLoader, get_component_factory, get_renderer_class, register_core_plugins, \
    create_rendering_context


class TestRendering(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()
        PluginLoader.load_plugin('mock_factories')
        PluginLoader.load_plugin('mock_rendering')

    def test_simple_rendering(self):
        context = create_rendering_context()
        component_factory = get_component_factory('mock')
        component: MockComponent = component_factory({'name': 'TEST', 'first_name': 'TEST2'})  # type: ignore
        renderer_class = get_renderer_class('mock_simple')
        renderer = renderer_class()
        self.assertIsInstance(renderer, MockRendererNoExpression)

        expected = "Mock[last_name='{}' first_name='{}']".format(component.name, component.first_name)
        actual = renderer.render(context, component)
        self.assertEqual(expected, actual)

    def test_rendering_with_data(self):
        data = {'person': {'first_name': 'Jean', 'last_name': 'DUPONT', 'phone': 'XXXXXXXXXXXX'}}
        variables = {'enterprise': 'Joe.CORP'}
        context = create_rendering_context(data=data, variables=variables)
        component_factory = get_component_factory('mock')
        component: MockComponent = component_factory(  # type: ignore
            {'name': '$.person.last_name', 'first_name': '$.person.first_name'})
        renderer_class = get_renderer_class('mock')
        renderer = renderer_class()
        self.assertIsInstance(renderer, MockRendererWithExpression)

        expected = "Mock[last_name='{}' first_name='{}']".format(data['person']['last_name'],
                                                                 data['person']['first_name'])
        actual = renderer.render(context, component)
        self.assertEqual(expected, actual)

    def test_nested(self):
        data = {'person': {'first_name': 'Jean', 'last_name': 'DUPONT', 'phone': 'XXXXXXXXXXXX'}}
        variables = {'enterprise': 'Joe.CORP'}
        context = create_rendering_context(data=data, variables=variables)

        component_factory = get_component_factory('mocks')
        component: MockParentComponent = component_factory(  # type: ignore
            {
                'destination': '~.enterprise',
                'mock_child': {'name': '$.person.last_name', 'first_name': '$.person.first_name'}
            }
        )

        renderer_class = get_renderer_class('mock_parent')
        renderer = renderer_class()
        self.assertIsInstance(renderer, MockParentRenderer)

        expected = "\n".join([
            "mock_parent '{}' ".format(variables['enterprise']) + "{",
            "\tMock[last_name='{}' first_name='{}']".format(data['person']['last_name'], data['person']['first_name']),
            "}"
        ])
        actual = renderer.render(context, component)
        self.assertEqual(expected, actual)
