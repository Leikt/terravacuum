import unittest

from terravacuum import register_core_plugins, get_component_factory, get_renderer_class, create_rendering_context
from terravacuum.core_plugins.terraform_generic.components import CommentComponent


class TestTGComments(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('comment')
        component = factory({'comments': ['First', 'Second']})
        self.assertIsInstance(component, CommentComponent)
        self.assertEqual(['First', 'Second'], component.comments)

    def test_inline(self):
        factory = get_component_factory('comment')
        component = factory('A comment')
        self.assertIsInstance(component, CommentComponent)
        self.assertEqual(['A comment'], component.comments)

    def test_list(self):
        factory = get_component_factory('comment')
        component = factory(['First', 'Second'])
        self.assertIsInstance(component, CommentComponent)
        self.assertEqual(['First', 'Second'], component.comments)

    def test_renderer(self):
        factory = get_component_factory('comment')
        component = factory(['First', 'Second'])
        context = create_rendering_context()

        renderer_c = get_renderer_class('comment')
        renderer = renderer_c()
        actual = renderer.render(context, component)
        expected = '# First\n# Second\n'
        self.assertEqual(expected, actual)

    def test_renderer_with_indent(self):
        factory = get_component_factory('comment')
        component = factory(['First', 'Second'])
        context = create_rendering_context()

        renderer_c = get_renderer_class('comment')
        renderer = renderer_c(1)
        actual = renderer.render(context, component)
        expected = '\t# First\n\t# Second\n'
        self.assertEqual(expected, actual)
