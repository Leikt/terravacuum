import unittest

from mock_factories import MockComponent
from terravacuum import register_plugin_sockets, PluginLoader, get_component_factory, get_renderer_class, Context, \
    register_core_plugins, PRenderer, BRACKET_CL, BRACKET_OP


class TestRenderer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        register_core_plugins()
        PluginLoader.load_plugin('mock_factories')
        PluginLoader.load_plugin('mock_renderer')

    def test_simple_renderer(self):
        factory = get_component_factory('mock')
        context = Context({}, {})
        component: MockComponent = factory({'name': 'TEST', 'first_name': 'TEST'})  # type: ignore
        renderer: PRenderer = get_renderer_class(component.get_renderer_name())(0)

        expected = f"mock_component {BRACKET_OP} name = {component.name} first_name = {component.first_name} {BRACKET_CL}"
        actual = renderer.render(context, component)
        self.assertEqual(expected, actual)

    def test_simple_renderer_with_expression(self):
        factory = get_component_factory('mock')
        context = Context({'name': 'TEST'}, {'name': 'TEST2'})
        component: MockComponent = factory({'name': '~.name', 'first_name': '$.name'})  # type: ignore
        renderer: PRenderer = get_renderer_class('mock_with_expression')(0)

        expected = f"mock_component {BRACKET_OP} name = {context.variables['name']} first_name = {context.data['name']} {BRACKET_CL}"
        actual = renderer.render(context, component)
        self.assertEqual(expected, actual)

    def test_render_child(self):
        pass

    def test_render_children(self):
        pass

    def test_render_multiple_data(self):
        pass
