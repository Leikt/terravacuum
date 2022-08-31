import os
import unittest

from terravacuum import register_core_plugins, get_component_factory, get_renderer_class, create_context, \
    load_file
from terravacuum.core_plugins.terraform_generic.components import FileComponent


class TestFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
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
        renderer_c = get_renderer_class(component.get_renderer_name())
        renderer = renderer_c(0)
        ctx_rendering = create_context()

        actual = renderer.render(ctx_rendering, component)  # type: ignore
        expected = ''
        self.assertEqual(expected, actual)
        self.assertTrue(os.path.isfile(component.destination))

        expected = """Name = Test
"""
        actual = load_file(component.destination)
        self.assertEqual(expected, actual)
