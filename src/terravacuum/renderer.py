import logging
from typing import Callable, Any

from .component import PComponent
from .context import Context
from .plugin_system import register_plugin_socket, plugin_registerer


class RendererNotFound(Exception):
    """Exception raised when a renderer is requested but not found."""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = 'No renderer is registered to the keyword "{}"'.format(keyword)
        super().__init__(self.message)


Renderer = Callable[[Context, PComponent], Any]
"""Renderer type."""

RendererRegistration = tuple[str, type]
"""Return type for the register_renderers plugin functions."""

@register_plugin_socket
class RendererPluginSocket:
    """Plugin socket for the components."""

    __renderers: dict[str, Renderer] = {}

    @classmethod
    @plugin_registerer('register_renderers')
    def register(cls, element):
        keyword, renderer = element
        if keyword in cls.__renderers:
            logging.warning('A renderer is already registered on keyword "{}"'.format(keyword))
            return

        cls.__renderers[keyword] = renderer

    @classmethod
    def get_renderer(cls, keyword: str) -> Renderer:
        if keyword not in cls.__renderers:
            raise RendererNotFound(keyword)
        return cls.__renderers[keyword]


def get_renderer(keyword: str) -> Renderer:
    """Get the renderer class from the given keyword"""
    return RendererPluginSocket.get_renderer(keyword)
