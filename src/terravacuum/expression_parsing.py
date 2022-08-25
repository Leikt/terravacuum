import logging
from enum import Enum
from typing import Protocol, Any, Optional

from terravacuum import Context


class ExpressionParsingResult(Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'
    NOT_PARSED = 'not_parsed'


class PExpressionParser(Protocol):
    """Object able to parse a string expression in the given context."""

    @staticmethod
    def parse(expr: str, context: Context) -> tuple[ExpressionParsingResult, Optional[Any]]:
        """Parse the expression and return the data."""


class ExpressionParserPluginSocket:
    """Plugin socket for the expression parsers."""

    __plugins: list[PExpressionParser] = []

    @classmethod
    def register(cls, module):
        if not hasattr(module, 'register_expression_parsers'):
            return
        for plugin in module.register_expression_parsers():
            if plugin in cls.__plugins:
                continue

            cls.__plugins.append(plugin)

    @classmethod
    def get_plugins(cls) -> list[PExpressionParser]:
        return cls.__plugins


def parse_expression(expr: str, context: Context) -> Optional[Any]:
    """Parse the given expression in the context.
    If no parser is able to parse the expression, it is return unchanged."""
    for plugin in ExpressionParserPluginSocket.get_plugins():
        code, result = plugin.parse(expr, context)
        if code == ExpressionParsingResult.SUCCESS:
            return result
        if code == ExpressionParsingResult.FAILURE:
            logging.error('Unable to parse the expression "{}"'.format(expr))
    return expr
