import unittest

from terravacuum import register_core_plugins, get_component_factory, get_renderer_class, create_rendering_context, \
    create_component_context
from terravacuum.core_plugins.terraform_generic.components import CommentComponent


class TestTGComments(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('comment')
        context = create_component_context()
        component = factory(context, {'comments': ['First', 'Second']})
        self.assertIsInstance(component, CommentComponent)
        self.assertEqual(['First', 'Second'], component.comments)

    def test_inline(self):
        factory = get_component_factory('comment')
        context = create_component_context()
        component = factory(context, 'A comment')
        self.assertIsInstance(component, CommentComponent)
        self.assertEqual(['A comment'], component.comments)

    def test_list(self):
        factory = get_component_factory('comment')
        context = create_component_context()
        component = factory(context, ['First', 'Second'])
        self.assertIsInstance(component, CommentComponent)
        self.assertEqual(['First', 'Second'], component.comments)

    def test_renderer(self):
        factory = get_component_factory('comment')
        ctx_component = create_component_context()
        component = factory(ctx_component, ['First', 'Second'])
        ctx_rendering = create_rendering_context()

        renderer_c = get_renderer_class('comment')
        renderer = renderer_c()
        actual = renderer.render(ctx_rendering, component)
        expected = '# First\n# Second\n'
        self.assertEqual(expected, actual)

    def test_renderer_with_indent(self):
        factory = get_component_factory('comment')
        ctx_component = create_component_context()
        component = factory(ctx_component, ['First', 'Second'])
        ctx_rendering = create_rendering_context()

        renderer_c = get_renderer_class('comment')
        renderer = renderer_c(1)
        actual = renderer.render(ctx_rendering, component)
        expected = '\t# First\n\t# Second\n'
        self.assertEqual(expected, actual)
