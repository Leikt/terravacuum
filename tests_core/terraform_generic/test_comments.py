import unittest

from terravacuum import get_component_factory, get_renderer, create_context, register_plugin_sockets
from terravacuum.core_plugins import register_core_plugins
from terravacuum.core_plugins.terraform_generic.components import CommentComponent


class TestTGComments(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('comment')
        context = create_context()
        component = factory(context, {'comments': ['First', 'Second']})
        self.assertIsInstance(component, CommentComponent)
        self.assertEqual(['First', 'Second'], component.comments)

    def test_inline(self):
        factory = get_component_factory('comment')
        context = create_context()
        component = factory(context, 'A comment')
        self.assertIsInstance(component, CommentComponent)
        self.assertEqual(['A comment'], component.comments)

    def test_list(self):
        factory = get_component_factory('comment')
        context = create_context()
        component = factory(context, ['First', 'Second'])
        self.assertIsInstance(component, CommentComponent)
        self.assertEqual(['First', 'Second'], component.comments)

    def test_renderer(self):
        factory = get_component_factory('comment')
        ctx_component = create_context()
        component = factory(ctx_component, ['First', 'Second'])
        ctx_rendering = create_context()

        renderer = get_renderer('comment')
        actual = renderer(ctx_rendering, component)
        expected = '# First\n# Second\n'
        self.assertEqual(expected, actual)

    def test_renderer_with_indent(self):
        factory = get_component_factory('comment')
        ctx_component = create_context()
        component = factory(ctx_component, ['First', 'Second'])
        ctx_rendering = create_context(indentation=1)

        renderer = get_renderer('comment')
        actual = renderer(ctx_rendering, component)
        expected = '\t# First\n\t# Second\n'
        self.assertEqual(expected, actual)
