import re
from typing import Optional, Any

from jsonpath_ng.ext import parse as parse_jsonpath

from terravacuum import PExpressionParser, Context, ExpressionParsingResult


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
            if re.search(template, expr):
                return parser(expr, context)
        return ExpressionParsingResult.NOT_PARSED, expr


def find_data(expr: str, dataset: Any) -> Optional[Any]:
    """Use the JsonPath to find data inside the dataset. If there is no matches it raises a KeyError."""
    found_data = parse_jsonpath(expr).find(dataset)
    if len(found_data) == 0:
        raise KeyError('No data matches the JsonPath "{}"'.format(expr))
    return found_data[0].value


def _parse(expr: str, context: Context, key: str):
    if key not in context:
        raise MissingContextKeyError(key, context)
    data = find_data(expr, context[key])
    return ExpressionParsingResult.SUCCESS, data


def parse_variable(expr: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
    """Parse the expression inside the variables."""
    return _parse('$' + expr[1:], context, 'variables')


def parse_data(expr: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
    """Parse the expression inside the data."""
    return _parse(expr, context, 'data')


def parse_nested(expression: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
    """Process nested expressions like "Name={{ $.employee.name }}" """
    expressions = re.findall(PATTERN_NESTED_EXPRESSION, expression)
    for full_expr, expr in expressions:
        _, value = CoreExpressionParer.parse(expr, context)
        expression = expression.replace(full_expr, str(value))
    return ExpressionParsingResult.SUCCESS, expression


PATTERN_NESTED_EXPRESSION = r'(\{\{ *(.*?) *\}\})'

PARSERS = {
    r'^\$\.': parse_data,
    r'^~\.': parse_variable,
    PATTERN_NESTED_EXPRESSION: parse_nested,
}
