import unittest

from mock_data2code.components import FunctionComponent
from terravacuum import register_core_plugins, PluginLoader, get_renderer, get_component_factory, \
    create_context

TEMPLATE = {
    'header': '$.name',
    'lines': [
        {'m2d-line': {'code': ['say_hello("{{$.persons.A}}")']}},
        {'m2d-line': 'say_goodbye("{{$.persons.B}}")'},
        {'m2d-line': ['x = {{ $.base_value }} + get_count()', 'new_var=yolooooooo']},
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

    # def test_renderer_factory(self):
    #     function_renderer_factory = get_renderer('function')
    #     function_renderer = function_renderer_factory(0)

    def test_render_function(self):
        # Component
        component_factory = get_component_factory('m2d-function')
        ctx_component = create_context()
        component = component_factory(ctx_component, TEMPLATE)
        self.assertIsInstance(component, FunctionComponent)

        ctx_rendering = create_context(data=DATA)

        function_renderer = get_renderer('m2d-function')

        actual = function_renderer(ctx_rendering, component)
        self.assertEqual(EXPECTED, actual)
