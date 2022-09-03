import unittest

from terravacuum import register_plugin_sockets
from terravacuum.context import create_context
from terravacuum.component import get_component_factory
from terravacuum.rendering import get_renderer
from terravacuum.core_plugins import register_core_plugins
from terravacuum.core_plugins.terraform_generic.components import ContainerComponent


class TestContainer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('include')
        ctx_component = create_context()
        component = factory(ctx_component, {'source': 'data_tests/test_include.yml'})
        self.assertIsInstance(component, ContainerComponent)
        self.assertEqual(1, len(component.children))
        self.assertEqual('George', component.children[0].__getattribute__('children')[0].__getattribute__('value'))
        self.assertEqual('MIETTAUX', component.children[0].__getattribute__('children')[1].__getattribute__('value'))

    def test_inline(self):
        factory = get_component_factory('include')
        ctx_component = create_context()
        component = factory(ctx_component, 'data_tests/test_include.yml')
        self.assertIsInstance(component, ContainerComponent)
        self.assertEqual(1, len(component.children))
        self.assertEqual('George', component.children[0].__getattribute__('children')[0].__getattribute__('value'))
        self.assertEqual('MIETTAUX', component.children[0].__getattribute__('children')[1].__getattribute__('value'))

    def test_renderer(self):
        factory = get_component_factory('include')
        ctx_component = create_context()
        component = factory(ctx_component, 'data_tests/test_include.yml')
        ctx_rendering = create_context()
        renderer = get_renderer('container')

        expected = """person {
\tLastName = George
\tFirstName = MIETTAUX
}
"""
        actual = renderer(ctx_rendering, component)
        self.assertEqual(expected, actual)
