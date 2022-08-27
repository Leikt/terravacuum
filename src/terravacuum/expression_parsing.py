import logging
from enum import Enum
from typing import Protocol, Any, Optional

from .plugin_system import register_plugin_socket, plugin_registerer
from .context import Context


class ExpressionParsingResult(Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'
    NOT_PARSED = 'not_parsed'


class PExpressionParser(Protocol):
    """Object able to parse a string expression in the given context."""

    @staticmethod
    def parse(expr: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
        """Parse the expression and return the data."""


@register_plugin_socket
class ExpressionParserPluginSocket:
    """Plugin socket for the expression parsers."""

    __plugins: list[PExpressionParser] = []

    @classmethod
    @plugin_registerer('register_expression_parsers')
    def register(cls, plugin):
        if plugin in cls.__plugins:
            return

        cls.__plugins.append(plugin)

    @classmethod
    def get_plugins(cls) -> list[PExpressionParser]:
        return cls.__plugins


def parse_expression(expr: str, context: Context, quote_string_with_spaces: bool = False) -> Optional[Any]:
    """Parse the given expression in the context.
    If no parser is able to parse the expression, it is return unchanged."""
    result = expr
    for plugin in ExpressionParserPluginSocket.get_plugins():
        code, result = plugin.parse(expr, context)
        if code == ExpressionParsingResult.FAILURE:
            logging.error('Unable to parse the expression "{}"'.format(expr))

    if isinstance(result, str) and quote_string_with_spaces and ' ' in result:
        result = "\"{}\"".format(result)
    return result
