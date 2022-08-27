import unittest

from terravacuum import register_core_plugins, get_component_factory, Context, get_renderer_class
from terravacuum.core_plugins.terraform_generic.components import BlankLinesComponent


class TestBlankLines(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('blank_lines')
        component = factory({'count': 3})
        self.assertIsInstance(component, BlankLinesComponent)
        self.assertEqual(3, component.count)

    def test_inline(self):
        factory = get_component_factory('blank_lines')
        component = factory('3')
        self.assertIsInstance(component, BlankLinesComponent)
        self.assertEqual(3, component.count)

    def test_renderer(self):
        factory = get_component_factory('blank_lines')
        component = factory('3')
        context = Context({}, {})
        renderer_c = get_renderer_class('blank_lines')
        renderer = renderer_c()
        actual = renderer.render(context, component)
        expected = "\n\n\n"
        self.assertEqual(expected, actual)
