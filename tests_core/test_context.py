import unittest

from terravacuum import create_context, Context


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
