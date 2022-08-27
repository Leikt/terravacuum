import unittest

from mock_data2code.components import FunctionComponent
from mock_data2code.renderers import FunctionRenderer
from terravacuum import register_core_plugins, PluginLoader, get_renderer_factory, get_component_factory, Context

TEMPLATE = {
    'header': 'name=$.name',
    'lines': [
        {'code_line': 'code="say_hello({{$.persons.A}})"'},
        {'code_line': 'code="say_goodbye({{$.persons.B}})"'},
        {'code_line': 'code="x = {{ $.base_value }} + get_count()"'},
    ]
}

DATA = {
    'name': 'do_something',
    'persons': {
        'A': 'George',
        'B': 'Pierrette'
    },
    'base_value': 5
}

EXPECTED = """function do_something() {
    say_hello(George)
    say_goodbye(Pierrette)
    x = 5 + get_count()
}
"""


class TestMockData2Code(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()
        PluginLoader.load_plugin('mock_data2code')

    def test_renderer_factory(self):
        function_renderer_factory = get_renderer_factory('function')
        function_renderer = function_renderer_factory(0)
        self.assertIsInstance(function_renderer, FunctionRenderer)

    def test_render_function(self):
        # Component
        component_factory = get_component_factory('function')
        component = component_factory(TEMPLATE)
        self.assertIsInstance(component, FunctionComponent)

        context = Context(DATA, {})

        function_renderer_factory = get_renderer_factory('function')
        function_renderer = function_renderer_factory(0)

        actual = function_renderer.render(context, component)

        print(EXPECTED)
        print()
        print(actual)
        self.assertEqual(EXPECTED, actual)
