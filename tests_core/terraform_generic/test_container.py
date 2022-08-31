import unittest

from terravacuum import register_core_plugins, get_component_factory, create_context, get_renderer_class
from terravacuum.core_plugins.terraform_generic.components import ContainerComponent


class TestContainer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
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
        renderer_c = get_renderer_class('container')
        renderer = renderer_c(0)

        expected = """person {
\tLastName = George
\tFirstName = MIETTAUX
}
"""
        actual = renderer.render(ctx_rendering, component)
        self.assertEqual(expected, actual)
