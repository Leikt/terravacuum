import unittest

from terravacuum import register_plugin_sockets, PluginLoader, parse_expression
from terravacuum.context import create_context


class TestExpressionParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        PluginLoader.load_plugin('plugins.core_expression_parser')

    def test_plain_expression(self):
        expr = 'SomePlainValue'
        context = create_context({}, {})
        parsed_expr = parse_expression(expr, context)
        self.assertEqual(expr, parsed_expr)

    def test_data_expression(self):
        data = {'name': 'Jean Dupont', 'age': 32}
        context = create_context(data, {})
        self.assertEqual(data['age'], parse_expression("$.age", context))
        self.assertEqual(data['name'], parse_expression("$.name", context))

    def test_variable_expression(self):
        variables = {'name': 'Jean Dupont', 'age': 32}
        context = create_context({}, variables)
        self.assertEqual(variables['age'], parse_expression("~.age", context))
        self.assertEqual(variables['name'], parse_expression("~.name", context))

    def test_nested_expression(self):
        data = {'name': 'Jean Dupont', 'age': 32}
        context = create_context(data, {})
        self.assertEqual(f"Name={data['name']}", parse_expression("Name={{ $.name }}", context))
        self.assertEqual(f"Age={data['age']} Name={data['name']}",
                         parse_expression("Age={{ $.age }} Name={{ $.name }}", context))

    def test_complex_nested_expression(self):
        data = {'name': 'Jean Dupont', 'age': 32}
        context = create_context(data, data)
        self.assertEqual(f"Age={data['age']} Name={data['name']}",
                         parse_expression("Age={{ $.age }} Name={{ ~.name }}", context))

    def test_key_error(self):
        context = create_context({'name': 'Jean Dupont', 'age': 32}, {})
        with self.assertRaises(KeyError):
            parse_expression('$.no_key', context)

    def test_complex_jsonpath(self):
        data = {"name": "some", "tags": [{"Key": "Name", "Value": "SOMEDATA"}]}
        context = create_context(data, {})
        expr = "$.tags[?(@.Key == 'Name')].Value"
        self.assertEqual(data['tags'][0]['Value'], parse_expression(expr, context))
