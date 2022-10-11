from typing import Any

from .renderer import get_renderer
from ..component import PComponent
from ..context import Context


def render_components(context: Context, components: list[PComponent]) -> list[Any]:
    """Render multiple components and return the result."""
    content = []
    for component in components:
        renderer = get_renderer(component.renderer)
        content.append(renderer(context, component))
    return content
