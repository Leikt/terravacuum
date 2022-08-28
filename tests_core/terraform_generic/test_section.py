import unittest

from terravacuum import register_core_plugins, get_component_factory, get_renderer_class, create_context
from terravacuum.core_plugins.terraform_generic.components import SectionComponent, HeaderComponent


class TestSection(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('section')
        component = factory({'header': {'keyword': 'instance', 'parameters': ['vm_name']}, 'children': [
            {'property': 'name=PA value=VA'},
            {'property': 'name=PB value=VB'}
        ]})
        self.assertIsInstance(component, SectionComponent)
        self.assertIsInstance(component.header, HeaderComponent)
        self.assertEqual(component.header.keyword, 'instance')
        self.assertEqual(component.children[0].name, 'PA')
        self.assertEqual(component.children[1].name, 'PB')

    def test_renderer(self):
        factory = get_component_factory('section')
        component = factory({'header': {'keyword': 'instance', 'parameters': ['vm_name']}, 'children': [
            {'property': 'name=PA value="V A"'},
            {'property': 'name=PB value=VB'}
        ]})
        renderer_c = get_renderer_class('section')
        renderer = renderer_c(0)

        expected = """instance "vm_name" {
\tPA = "V A"
\tPB = VB
}
"""
        actual = renderer.render(create_context({}, {}), component)
        self.assertEqual(expected, actual)

    def test_renderer_indent(self):
        factory = get_component_factory('section')
        component = factory({'header': {'keyword': 'instance', 'is_property': True}, 'children': [
            {'blank_lines': '1'},
            {'comment': 'Some properties...'},
            {'property': 'name=PA value="V A"'},
            {'property': 'name=PB value=VB'}
        ]})
        renderer_c = get_renderer_class('section')
        renderer = renderer_c(1)

        expected = """\tinstance = {
\t\t
\t\t# Some properties...
\t\tPA = "V A"
\t\tPB = VB
\t}
"""
        actual = renderer.render(create_context({}, {}), component)
        self.assertEqual(expected, actual)