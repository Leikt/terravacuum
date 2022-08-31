from typing import Any

from .renderer import get_renderer_class
from .component import PComponent
from .context import Context


def tab(count: int) -> str:
    return '\t' * count


def render_components(context: Context, components: list[PComponent], *args, **kwargs) -> list[Any]:
    """Render multiple components and return the result."""
    content = []
    for component in components:
        renderer_c = get_renderer_class(component.get_renderer_name())
        renderer = renderer_c(*args, **kwargs)
        content.append(renderer.render(context, component))
    return content
