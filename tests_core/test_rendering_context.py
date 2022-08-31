import unittest

from terravacuum import create_rendering_context, RenderingContext


class TestRenderingContext(unittest.TestCase):
    def test_creation(self):
        context = create_rendering_context()
        self.assertIsInstance(context, RenderingContext)
        self.assertIsInstance(context.variables, dict)
        self.assertIsInstance(context.data, dict)

    def test_create_with_parameters(self):
        context = create_rendering_context(data={'value': 1})
        self.assertIsInstance(context.data, dict)
        self.assertEqual(1, context.data['value'])

    def test_create_from_parent(self):
        context = create_rendering_context(data={'value': 1})
        context_child = create_rendering_context(parent=context, data={'child_v': 12})
        self.assertIsInstance(context_child, RenderingContext)
        self.assertEqual(12, context_child.data['child_v'])

    def test_others(self):
        context = create_rendering_context()
        context['test'] = 12
        self.assertEqual(12, context['test'])

    def test_others_inheritance(self):
        context = create_rendering_context(others={'test': 'something'})
        child_context = create_rendering_context(parent=context)
        self.assertEqual('something', child_context['test'])
