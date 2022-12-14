import unittest

from mock_factories import MockComponent, MockParentComponent
from terravacuum import register_plugin_sockets
from terravacuum.core_plugins import register_core_plugins
from terravacuum.plugin_system import PluginLoader
from terravacuum.rendering import RendererNotFound, get_renderer
from terravacuum.context import create_context
from terravacuum.component import get_component_factory


class TestRendering(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        register_core_plugins()
        PluginLoader.load_plugin('mock_factories')
        PluginLoader.load_plugin('mock_rendering')

    def test_not_found(self):
        with self.assertRaises(RendererNotFound):
            get_renderer('not_found')

    def test_simple_rendering(self):
        ctx_rendering = create_context()
        ctx_component = create_context()
        component_factory = get_component_factory('mock')
        component: MockComponent = component_factory(  # type: ignore
            ctx_component,
            {'name': 'TEST', 'first_name': 'TEST2'})

        renderer = get_renderer('mock_simple')
        expected = "Mock[last_name='{}' first_name='{}']".format(component.name, component.first_name)
        actual = renderer(ctx_rendering, component)
        self.assertEqual(expected, actual)

    def test_rendering_with_data(self):
        data = {'person': {'first_name': 'Jean', 'last_name': 'DUPONT', 'phone': 'XXXXXXXXXXXX'}}
        variables = {'enterprise': 'Joe.CORP'}
        ctx_rendering = create_context(data=data, variables=variables)
        ctx_component = create_context()
        component_factory = get_component_factory('mock')
        component: MockComponent = component_factory(  # type: ignore
            ctx_component,
            {'name': '$.person.last_name',
             'first_name': '$.person.first_name'})

        renderer = get_renderer('mock')
        expected = "Mock[last_name='{}' first_name='{}']".format(data['person']['last_name'],
                                                                 data['person']['first_name'])
        actual = renderer(ctx_rendering, component)
        self.assertEqual(expected, actual)

    def test_nested(self):
        data = {'person': {'first_name': 'Jean', 'last_name': 'DUPONT', 'phone': 'XXXXXXXXXXXX'}}
        variables = {'enterprise': 'Joe.CORP'}
        ctx_rendering = create_context(data=data, variables=variables)
        ctx_component = create_context()

        component_factory = get_component_factory('mocks')
        component: MockParentComponent = component_factory(  # type: ignore
            ctx_component,
            {
                'destination': '~.enterprise',
                'mock_child': {'name': '$.person.last_name',
                               'first_name': '$.person.first_name'}
            }
        )

        renderer = get_renderer('mock_parent')
        expected = "\n".join([
            "mock_parent '{}' ".format(variables['enterprise']) + "{",
            "\tMock[last_name='{}' first_name='{}']".format(data['person']['last_name'], data['person']['first_name']),
            "}"
        ])
        actual = renderer(ctx_rendering, component)
        self.assertEqual(expected, actual)
