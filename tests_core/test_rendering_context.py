import os
import unittest

from terravacuum import create_rendering_context, RenderingContext


class TestRenderingContext(unittest.TestCase):
    def test_creation(self):
        context = create_rendering_context()
        self.assertIsInstance(context, RenderingContext)
        self.assertIsInstance(context.variables, dict)
        self.assertIsInstance(context.data, dict)
        self.assertEqual(os.getcwd(), context.working_directory)

    def test_create_with_parameters(self):
        context = create_rendering_context(data={'value': 1})
        self.assertIsInstance(context.data, dict)
        self.assertEqual(1, context.data['value'])

    def test_create_from_parent(self):
        context = create_rendering_context(data={'value': 1}, working_directory='/test')
        context_child = create_rendering_context(parent=context, data={'child_v': 12})
        self.assertIsInstance(context_child, RenderingContext)
        self.assertEqual(12, context_child.data['child_v'])
        self.assertEqual('/test', context_child.working_directory)
