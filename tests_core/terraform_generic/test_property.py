import unittest

from terravacuum import register_core_plugins, get_component_factory, get_renderer_class, Context
from terravacuum.core_plugins.terraform_generic.components import PropertyComponent


class TestProperty(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('property')
        component = factory({'name': 'PropertyA', 'value': 'ValueA'})
        self.assertIsInstance(component, PropertyComponent)
        self.assertEqual('PropertyA', component.name)
        self.assertEqual('ValueA', component.value)

    def test_inline(self):
        factory = get_component_factory('property')
        component = factory('name=PropertyA value=ValueA')
        self.assertIsInstance(component, PropertyComponent)
        self.assertEqual('PropertyA', component.name)
        self.assertEqual('ValueA', component.value)

    def test_renderer(self):
        factory = get_component_factory('property')
        component: PropertyComponent = factory('name=PropertyA value=ValueA')  # type: ignore
        renderer_c = get_renderer_class('property')
        renderer = renderer_c(0)

        expected = f"{component.name} = {component.value}"
        actual = renderer.render(Context({}, {}), component)
        self.assertEqual(expected, actual)

        renderer_indent = renderer_c(1)
        expected = f"\t{component.name} = {component.value}"
        actual = renderer_indent.render(Context({}, {}), component)
        self.assertEqual(expected, actual)
