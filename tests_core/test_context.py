import unittest

from terravacuum import create_context, Context, register_core_plugins, parse_expression
from terravacuum.core_plugins.expression_parser import MissingContextKeyError


class TestContext(unittest.TestCase):
    def test_empty(self):
        context = create_context()
        self.assertIsInstance(context, Context)
        self.assertEqual(0, len(context))

    def test_simple(self):
        context = create_context(data={'sound': 'vrooom'})
        self.assertEqual('vrooom', context['data']['sound'])

    def test_inheritance(self):
        ctx_parent = create_context(data={'sound': 'vrooom'})
        ctx_child = create_context(ctx_parent, new_sound='booooom')
        self.assertIsInstance(ctx_child, Context)
        self.assertEqual('booooom', ctx_child['new_sound'])
        self.assertEqual('vrooom', ctx_child['data']['sound'])

    def test_missing_error(self):
        register_core_plugins()
        context = create_context()
        with self.assertRaises(MissingContextKeyError):
            parse_expression('$.do_not_exists', context)
