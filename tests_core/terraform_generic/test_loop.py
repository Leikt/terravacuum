import unittest

from terravacuum import register_core_plugins, get_component_factory, get_renderer, create_context
from terravacuum.core_plugins.terraform_generic.components import LoopComponent, PropertyComponent


class TestLoop(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()

    def test_component(self):
        factory = get_component_factory('loop')
        ctx_component = create_context()
        component = factory(
            ctx_component,
            {'through': '$.instances', 'children': [{'property': 'name=Name value="{{~.client}} - {{$.name}}"'}]})
        self.assertIsInstance(component, LoopComponent)
        self.assertEqual('$.instances', component.through)
        self.assertEqual(1, len(component.children))
        self.assertIsInstance(component.children[0], PropertyComponent)

    def test_renderer(self):
        factory = get_component_factory('loop')
        ctx_component = create_context()
        component = factory(
            ctx_component,
            {'through': '$.instances', 'children': [{'property': 'name=Name value="{{~.client}} - {{$.name}}"'}]})
        data = {'instances': [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}]}
        variables = {'client': 'D.CORP'}
        ctx_rendering = create_context(data=data, variables=variables)
        renderer = get_renderer('loop')
        expected = """Name = "D.CORP - A"
Name = "D.CORP - B"
Name = "D.CORP - C"
"""
        actual = renderer(ctx_rendering, component)
        self.assertEqual(expected, actual)

        ctx_rendering = create_context(parent=ctx_rendering, indentation=2)
        expected = """\t\tName = "D.CORP - A"
\t\tName = "D.CORP - B"
\t\tName = "D.CORP - C"
"""
        actual = renderer(ctx_rendering, component)
        self.assertEqual(expected, actual)
