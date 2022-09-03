import unittest

from terravacuum.context import create_context, Context, FrozenContextError
from terravacuum.expression_parsing import parse_expression
from terravacuum.core_plugins import register_core_plugins
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

    def test_modification_forbidden(self):
        context = create_context(some='thing', nest={'data': 12})
        self.assertEqual('thing', context['some'])
        self.assertEqual(12, context['nest']['data'])
        with self.assertRaises(FrozenContextError):
            context['some'] = 12
        # with self.assertRaises(FrozenContextError):
        #     context['nest']['data'] = 13
