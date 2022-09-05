import logging
from enum import Enum
from typing import Protocol, Any, Optional

from ..plugin_system import PluginLoader
from ..context import Context


class ExpressionParsingResult(Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'
    NOT_PARSED = 'not_parsed'


class PExpressionParser(Protocol):
    """Object able to parse a string expression in the given context."""

    @staticmethod
    def parse(expr: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
        """Parse the expression and return the data."""


def parse_expression(expr: str, context: Context,
                     quote_string_with_spaces: bool = False,
                     first: bool = True
                     ) -> Optional[Any]:
    """Parse the given expression in the context.
    If no parser is able to parse the expression, it is return unchanged."""
    result = expr
    for _, parser in PluginLoader.get('expression_parser'):
        code, result = parser.parse(expr, context)
        if code == ExpressionParsingResult.FAILURE:
            logging.error('Unable to parse the expression "{}"'.format(expr))

    if first and isinstance(result, list):
        result = result[0]

    if isinstance(result, str) and quote_string_with_spaces and ' ' in result:
        result = "\"{}\"".format(result)
    return result
