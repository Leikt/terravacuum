from typing import Any

from .component import PComponent
from .context import Context

TAB = '\t'
BRACKET_OP = '{'
BRACKET_CL = '}'


def render_children(context: Context, children: list[PComponent]) -> Any:
    """Render a list of components."""
