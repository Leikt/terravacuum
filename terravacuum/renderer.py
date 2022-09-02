from typing import Callable, Any

from .component import PComponent
from .context import Context
from .plugin_system import PluginLoader, PluginItemNotFoundError


class RendererNotFound(PluginItemNotFoundError):
    """Exception raised when a renderer is requested but not found."""


Renderer = Callable[[Context, PComponent], Any]
"""Renderer type."""

RendererRegistration = tuple[str, type]
"""Return type for the register_renderers plugin functions."""


def get_renderer(keyword: str) -> Renderer:
    """Get the renderer class from the given keyword"""
    return PluginLoader.get('renderer')[keyword]
