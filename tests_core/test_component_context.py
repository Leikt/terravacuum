import unittest

from terravacuum import create_component_context, ComponentContext


class TestComponentContext(unittest.TestCase):
    def test_creation(self):
        context = create_component_context()
        self.assertIsInstance(context, ComponentContext)

    def test_create_from_parent(self):
        context = create_component_context()
        context_child = create_component_context(parent=context)
        self.assertIsInstance(context_child, ComponentContext)

    def test_others(self):
        context = create_component_context()
        context['test'] = 12
        self.assertEqual(12, context['test'])

    def test_others_inheritance(self):
        context = create_component_context(others={'test': 'something'})
        child_context = create_component_context(parent=context)
        self.assertEqual('something', child_context['test'])
