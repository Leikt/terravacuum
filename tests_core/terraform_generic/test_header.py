import unittest

from terravacuum import register_core_plugins, get_component_factory, get_renderer_class, create_rendering_context, \
    create_component_context
from terravacuum.core_plugins.terraform_generic.components import HeaderComponent


class TestHeader(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('header')
        ctx_component = create_component_context()
        component = factory(ctx_component, {'keyword': 'instance', 'parameters': ['vm_name'], 'is_property': True})
        self.assertIsInstance(component, HeaderComponent)
        self.assertEqual('instance', component.keyword)
        self.assertEqual(['vm_name'], component.parameters)
        self.assertEqual(True, component.is_property)

    def test_inline(self):
        factory = get_component_factory('header')
        ctx_component = create_component_context()
        component = factory(ctx_component, 'instance')
        self.assertIsInstance(component, HeaderComponent)
        self.assertEqual('instance', component.keyword)
        self.assertEqual([], component.parameters)
        self.assertEqual(False, component.is_property)

    def test_renderer(self):
        factory = get_component_factory('header')
        renderer_c = get_renderer_class('header')
        ctx_rendering = create_rendering_context()
        ctx_component = create_component_context()

        component = factory(ctx_component, 'instance')
        renderer = renderer_c(0)
        self.assertEqual("instance {\n", renderer.render(ctx_rendering, component))

        component = factory(ctx_component, {'keyword': 'instance', 'parameters': ['vm_name'], 'is_property': True})
        renderer = renderer_c(1)
        self.assertEqual("\tinstance \"vm_name\" = {\n", renderer.render(ctx_rendering, component))
