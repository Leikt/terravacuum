import unittest

from terravacuum import register_core_plugins, get_component_factory, get_renderer_class, create_context
from terravacuum.core_plugins.terraform_generic.components import HeaderComponent


class TestHeader(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('header')
        component = factory({'keyword': 'instance', 'parameters': ['vm_name'], 'is_property': True})
        self.assertIsInstance(component, HeaderComponent)
        self.assertEqual('instance', component.keyword)
        self.assertEqual(['vm_name'], component.parameters)
        self.assertEqual(True, component.is_property)

    def test_inline(self):
        factory = get_component_factory('header')
        component = factory('instance')
        self.assertIsInstance(component, HeaderComponent)
        self.assertEqual('instance', component.keyword)
        self.assertEqual([], component.parameters)
        self.assertEqual(False, component.is_property)

    def test_renderer(self):
        factory = get_component_factory('header')
        renderer_c = get_renderer_class('header')
        context = create_context({}, {})

        component = factory('instance')
        renderer = renderer_c(0)
        self.assertEqual("instance {\n", renderer.render(context, component))

        component = factory({'keyword': 'instance', 'parameters': ['vm_name'], 'is_property': True})
        renderer = renderer_c(1)
        self.assertEqual("\tinstance \"vm_name\" = {\n", renderer.render(context, component))