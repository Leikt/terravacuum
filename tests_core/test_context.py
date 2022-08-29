import os
import unittest

from terravacuum import create_rendering_context, RenderingContext


class TestContext(unittest.TestCase):
    def test_creation(self):
        context = create_rendering_context()
        self.assertIsInstance(context, RenderingContext)
        self.assertIsInstance(context.variables, dict)
        self.assertIsInstance(context.data, dict)
        self.assertEqual(os.getcwd(), context.working_directory)
