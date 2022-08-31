import os
import unittest

from terravacuum import create_component_context, ComponentContext


class TestComponentContext(unittest.TestCase):
    def test_creation(self):
        context = create_component_context()
        self.assertIsInstance(context, ComponentContext)
        self.assertIsInstance(context.working_directory, str)
        self.assertEqual(os.getcwd(), context.working_directory)

    def test_create_with_parameters(self):
        context = create_component_context(working_directory='/test')
        self.assertEqual('/test', context.working_directory)

    def test_create_from_parent(self):
        context = create_component_context(working_directory='/test')
        context_child = create_component_context(parent=context)
        self.assertIsInstance(context_child, ComponentContext)
        self.assertEqual('/test', context_child.working_directory)
