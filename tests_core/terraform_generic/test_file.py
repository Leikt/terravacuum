import os
import unittest

from terravacuum import get_component_factory, get_renderer, create_context, \
    load_file, register_plugin_sockets
from terravacuum.core_plugins import register_core_plugins
from terravacuum.core_plugins.terraform_generic.components import FileComponent


class TestFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        register_core_plugins()

    def test_normal(self):
        factory = get_component_factory('file')
        ctx_component = create_context()
        component = factory(
            ctx_component,
            {'destination': 'data_tests/created_file.tf', 'children': [{'property': 'name=Name value=Test'}]})
        self.assertIsInstance(component, FileComponent)
        self.assertEqual('data_tests/created_file.tf', component.destination)
        self.assertEqual(1, len(component.children))

    def test_renderer(self):
        factory = get_component_factory('file')
        ctx_component = create_context()
        component = factory(
            ctx_component,
            {'destination': 'data_tests/created_file.tf', 'children': [{'property': 'name=Name value=Test'}]})
        self.assertIsInstance(component, FileComponent)
        renderer = get_renderer(component.renderer)
        ctx_rendering = create_context()

        actual = renderer(ctx_rendering, component)  # type: ignore
        expected = ''
        self.assertEqual(expected, actual)
        self.assertTrue(os.path.isfile(component.destination))

        expected = """Name = Test
"""
        actual = load_file(component.destination)
        self.assertEqual(expected, actual)
