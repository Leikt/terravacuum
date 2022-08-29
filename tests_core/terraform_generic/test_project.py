import unittest

from terravacuum import register_core_plugins, get_component_factory, get_renderer_class, create_context, load_file
from terravacuum.core_plugins.terraform_generic.components import ProjectComponent


class TestProject(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()

    def test_component(self):
        factory = get_component_factory('project')
        component = factory({'directory': 'data_tests/project_test/', 'children': [
            {'file': {'destination': 'test.tf', 'children': [{'property': 'name=Name value=TEST'}]}}]})
        self.assertIsInstance(component, ProjectComponent)
        self.assertEqual('data_tests/project_test/', component.directory)
        self.assertEqual(1, len(component.children))

    def test_renderer(self):
        factory = get_component_factory('project')
        component = factory({'directory': 'data_tests/project_test/', 'children': [
            {'file': {'destination': 'test.tf', 'children': [{'property': 'name=Name value=TEST'}]}}]})
        self.assertIsInstance(component, ProjectComponent)
        context = create_context({}, {})

        renderer_c = get_renderer_class(component.get_renderer_name())
        renderer = renderer_c()

        expected = ''
        actual = renderer.render(context, component)
        self.assertEqual(expected, actual)

        expected = """Name = TEST
"""
        actual = load_file('data_tests/project_test/test.tf')
        self.assertEqual(expected, actual)