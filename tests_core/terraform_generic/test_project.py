import os
import shutil
import unittest

from terravacuum import register_plugin_sockets
from terravacuum.context import create_context
from terravacuum.component import get_component_factory
from terravacuum.rendering import get_renderer
from terravacuum.files import load_file
from terravacuum.core_plugins import register_core_plugins
from terravacuum.core_plugins.terraform_generic.components import ProjectComponent


class TestProject(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        register_core_plugins()
        if os.path.exists('data_tests/project_test'):
            shutil.rmtree('data_tests/project_test')

    def test_component(self):
        factory = get_component_factory('project')
        ctx_component = create_context()
        component = factory(ctx_component, {'directory': 'data_tests/project_test/', 'children': [
            {'file': {'destination': 'test.tf', 'children': [{'property': 'name=Name value=TEST'}]}}]})
        self.assertIsInstance(component, ProjectComponent)
        self.assertEqual(1, len(component.children))

    def test_renderer(self):
        factory = get_component_factory('project')
        ctx_component = create_context()
        component = factory(
            ctx_component,
            {'directory': 'data_tests/project_test/', 'children': [
                {'file': {'destination': 'prop/test2.tf', 'children': [{'property': 'name=Name value=TEST'}]}}]})
        self.assertIsInstance(component, ProjectComponent)
        ctx_rendering = create_context()

        renderer = get_renderer(component.renderer)

        expected = ''
        actual = renderer(ctx_rendering, component)
        self.assertEqual(expected, actual)

        expected = """Name = TEST
"""
        actual = load_file('data_tests/project_test/prop/test2.tf')
        self.assertEqual(expected, actual)
