import unittest

from mock_data2code.components import FunctionComponent
from mock_data2code.renderers import FunctionRenderer
from terravacuum import register_core_plugins, PluginLoader, get_renderer_factory, get_component_factory, \
    create_context

TEMPLATE = {
    'header': '$.name',
    'lines': [
        {'code_line': {'code': ['say_hello("{{$.persons.A}}")']}},
        {'code_line': 'say_goodbye("{{$.persons.B}}")'},
        {'code_line': ['x = {{ $.base_value }} + get_count()', 'new_var=yolooooooo']},
    ],
    'quick_lines': [
        'hello = print("hello")',
        'do_something()'
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
\tsay_hello("George")
\tsay_goodbye("Pierrette")
\tx = 5 + get_count()
\tnew_var=yolooooooo
\thello = print("hello")
\tdo_something()
}"""


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
        context = create_context()
        component = component_factory(context, TEMPLATE)
        self.assertIsInstance(component, FunctionComponent)

        context = create_context(data=DATA)

        function_renderer_factory = get_renderer_factory('function')
        function_renderer = function_renderer_factory(0)

        actual = function_renderer.render(context, component)
        self.assertEqual(EXPECTED, actual)
