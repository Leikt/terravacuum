import unittest

from terravacuum.context import create_context, Context


class TestContext(unittest.TestCase):
    def test_creation(self):
        context = create_context({}, {})
        self.assertIsInstance(context, Context)
        self.assertIsInstance(context.variables, dict)
        self.assertIsInstance(context.data, dict)
