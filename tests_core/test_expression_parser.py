import unittest

from terravacuum import register_plugin_sockets
from terravacuum.plugin_system import PluginLoader
from terravacuum.context import create_context
from terravacuum.expression_parsing import parse_expression


class TestExpressionParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        PluginLoader.load_plugin('terravacuum.core_plugins.expression_parser')

    def test_plain_expression(self):
        expr = 'SomePlainValue'
        context = create_context()
        parsed_expr = parse_expression(expr, context)
        self.assertEqual(expr, parsed_expr)

    def test_data_expression(self):
        data = {'name': 'Jean Dupont', 'age': 32}
        context = create_context(data=data)
        self.assertEqual(data['age'], parse_expression("$.age", context))
        self.assertEqual(data['name'], parse_expression("$.name", context))

    def test_variable_expression(self):
        variables = {'name': 'Jean Dupont', 'age': 32}
        context = create_context(variables=variables)
        self.assertEqual(variables['age'], parse_expression("~.age", context))
        self.assertEqual(variables['name'], parse_expression("~.name", context))

    def test_nested_expression(self):
        data = {'name': 'Jean Dupont', 'age': 32}
        context = create_context(data=data)
        self.assertEqual(f"Name={data['name']}", parse_expression("$$.Name={{ $.name }}", context))
        self.assertEqual(f"Age={data['age']} Name={data['name']}",
                         parse_expression("$$.Age={{ $.age }} Name={{ $.name }}", context))

    def test_complex_nested_expression(self):
        data = {'name': 'Jean Dupont', 'age': 32}
        context = create_context(data=data, variables=data)
        self.assertEqual(f"Age={data['age']} Name={data['name']}",
                         parse_expression("$$.Age={{ $.age }} Name={{ ~.name }}", context))

    def test_key_error(self):
        context = create_context(data={'name': 'Jean Dupont', 'age': 32})
        with self.assertRaises(KeyError):
            parse_expression('$.no_key', context)

    def test_complex_jsonpath(self):
        data = {"name": "some", "tags": [{"Key": "Name", "Value": "SOMEDATA"}]}
        context = create_context(data=data)
        expr = "$.tags[?(@.Key == 'Name')].Value"
        self.assertEqual(data['tags'][0]['Value'], parse_expression(expr, context))

    def test_quote_string(self):
        expr = "some word with spaces"
        result = parse_expression(expr, create_context(), True)
        self.assertEqual("\"{}\"".format(expr), result)

    def test_raw_expression_parser(self):
        data = {
            'objects': [
                {'v': 1},
                {'v': 'a'},
                {'v': True},
            ]
        }
        expr = '$R.objects[*].v'
        expected = [1, 'a', True]
        actual = parse_expression(expr, create_context(data=data))
        self.assertEqual(expected, actual)

        expr = '~R.objects[*].v'
        actual = parse_expression(expr, create_context(variables=data))
        self.assertEqual(expected, actual)
