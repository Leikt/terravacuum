import unittest

from terravacuum import register_plugin_sockets
from terravacuum.context import create_context
from terravacuum.component import get_component_factory
from terravacuum.rendering import get_renderer
from terravacuum.core_plugins import register_core_plugins
from terravacuum.core_plugins.terraform_generic.components import BlankLinesComponent


class TestBlankLines(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('blank_lines')
        context = create_context()
        component = factory(context, {'count': 3})
        self.assertIsInstance(component, BlankLinesComponent)
        self.assertEqual(3, component.count)

    def test_inline(self):
        factory = get_component_factory('blank_lines')
        context = create_context()
        component = factory(context, '3')
        self.assertIsInstance(component, BlankLinesComponent)
        self.assertEqual(3, component.count)

    def test_renderer(self):
        factory = get_component_factory('blank_lines')
        context = create_context()
        component = factory(context, '3')
        context = create_context()
        renderer = get_renderer('blank_lines')
        actual = renderer(context, component)
        expected = "\n\n\n"
        self.assertEqual(expected, actual)
