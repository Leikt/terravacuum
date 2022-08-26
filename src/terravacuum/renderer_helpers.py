from typing import Any

from .component import PComponent
from .context import Context


def render_children(context: Context, children: list[PComponent]) -> Any:
    """Render a list of components."""
