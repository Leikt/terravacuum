import re
from typing import Optional, Any

from jsonpath_ng.ext import parse as parse_jsonpath

from terravacuum.expression_parsing import PExpressionParser, ExpressionParsingResult
from terravacuum.context import Context


class MissingContextKeyError(Exception):
    """Exception raised when a context miss required information."""

    def __init__(self, key: str, context: Context):
        self.key = key
        self.context = context
        self.message = f"Missing key '{key}' in the context :\n{context}"
        super().__init__(self.message)


def register_expression_parsers() -> tuple[str, PExpressionParser]:
    """Function called by the plugin loader to register the expression parsers."""
    yield 'terravacuum-core', CoreExpressionParer


class CoreExpressionParer:
    @staticmethod
    def parse(expr: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
        for template, parser in PARSERS.items():
            if not expr.startswith(template):
                continue
            return parser(expr, context)
        return ExpressionParsingResult.NOT_PARSED, expr


def find_data(expr: str, dataset: Any) -> list[Any]:
    """Use the JsonPath to find data inside the dataset. If there is no matches it raises a KeyError."""
    found_data = parse_jsonpath(expr).find(dataset)
    if len(found_data) == 0:
        raise KeyError('No data matches the JsonPath "{}"\nDataset:\n{}'.format(expr, dataset))
    return list(map(lambda x: x.value, found_data))


def _parse(expr: str, context: Context, key: str) -> tuple[ExpressionParsingResult, list[Any]]:
    if key not in context:
        raise MissingContextKeyError(key, context)
    data = find_data(expr, context[key])
    return ExpressionParsingResult.SUCCESS, data


def parse_variable(expr: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
    """Parse the expression inside the variables."""
    code, result = _parse('$' + expr[1:], context, 'variables')
    return code, result[0]


def parse_data(expr: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
    """Parse the expression inside the data."""
    code, result = _parse(expr, context, 'data')
    return code, result[0]


def parse_raw_data(expr: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
    return _parse('$' + expr[2:], context, 'data')


def parser_raw_variable(expr: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
    return _parse('$' + expr[2:], context, 'variables')


def parse_nested(expression: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
    """Process nested expressions like "$$.Name={{ $.employee.name }}" """
    expression = expression[3:]
    expressions = re.findall(PATTERN_NESTED_EXPRESSION, expression)
    for full_expr, expr in expressions:
        _, value = CoreExpressionParer.parse(expr, context)
        expression = expression.replace(full_expr, str(value))
    return ExpressionParsingResult.SUCCESS, expression


PATTERN_NESTED_EXPRESSION = r'(\{\{ *(.*?) *\}\})'

PARSERS = {
    '$.': parse_data,
    '~.': parse_variable,
    '$R.': parse_raw_data,
    '~R.': parser_raw_variable,
    '$$.': parse_nested,
}
