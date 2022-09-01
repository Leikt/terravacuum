import unittest

from terravacuum import get_component_factory, get_renderer, create_context, register_plugin_sockets
from terravacuum.core_plugins import register_core_plugins
from terravacuum.core_plugins.terraform_generic.components import HeaderComponent


class TestHeader(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('header')
        ctx_component = create_context()
        component = factory(ctx_component, {'keyword': 'instance', 'parameters': ['vm_name'], 'is_property': True})
        self.assertIsInstance(component, HeaderComponent)
        self.assertEqual('instance', component.keyword)
        self.assertEqual(['vm_name'], component.parameters)
        self.assertEqual(True, component.is_property)

    def test_inline(self):
        factory = get_component_factory('header')
        ctx_component = create_context()
        component = factory(ctx_component, 'instance')
        self.assertIsInstance(component, HeaderComponent)
        self.assertEqual('instance', component.keyword)
        self.assertEqual([], component.parameters)
        self.assertEqual(False, component.is_property)

    def test_renderer(self):
        factory = get_component_factory('header')
        renderer = get_renderer('header')
        ctx_rendering = create_context()
        ctx_component = create_context()

        component = factory(ctx_component, 'instance')
        self.assertEqual("instance {\n", renderer(ctx_rendering, component))

        component = factory(ctx_component, {'keyword': 'instance', 'parameters': ['vm_name'], 'is_property': True})
        ctx_rendering = create_context(parent=ctx_component, indentation=1)
        self.assertEqual("\tinstance \"vm_name\" = {\n", renderer(ctx_rendering, component))
