import unittest

from terravacuum import register_core_plugins, get_component_factory, get_renderer, create_context
from terravacuum.core_plugins.terraform_generic.components import PropertyComponent


class TestProperty(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('property')
        ctx_component = create_context()
        component = factory(ctx_component, {'name': 'PropertyA', 'value': 'ValueA'})
        self.assertIsInstance(component, PropertyComponent)
        self.assertEqual('PropertyA', component.name)
        self.assertEqual('ValueA', component.value)

    def test_inline(self):
        factory = get_component_factory('property')
        ctx_component = create_context()
        component = factory(ctx_component, 'name=PropertyA value=ValueA')
        self.assertIsInstance(component, PropertyComponent)
        self.assertEqual('PropertyA', component.name)
        self.assertEqual('ValueA', component.value)

    def test_renderer(self):
        factory = get_component_factory('property')
        ctx_component = create_context()
        component: PropertyComponent = factory(ctx_component, 'name="Property A" value=ValueA')  # type: ignore
        renderer = get_renderer('property')

        expected = f"\"{component.name}\" = {component.value}\n"
        actual = renderer(create_context(), component)
        self.assertEqual(expected, actual)

        expected = f"\t\"{component.name}\" = {component.value}\n"
        actual = renderer(create_context(indentation=1), component)
        self.assertEqual(expected, actual)
