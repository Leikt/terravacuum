import logging
from typing import Protocol, Callable, Any

from .component import PComponent
from .rendering_context import RenderingContext
from .plugin_system import register_plugin_socket, plugin_registerer


class RendererNotFound(Exception):
    """Exception raised when a renderer is requested but not found."""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = 'No renderer is registered to the keyword "{}"'.format(keyword)
        super().__init__(self.message)


RendererRegistration = tuple[str, type]
"""Return type for the register_renderers plugin functions."""


class PRenderer(Protocol):
    """A component of the template, it is able to process data to a renderer"""

    def get_renderer_name(self) -> str:
        """Return the name of the component's renderer."""

    def render(self, context: RenderingContext, component: PComponent) -> Any:
        """Render the given component in the context."""


@register_plugin_socket
class RendererPluginSocket:
    """Plugin socket for the components."""

    __renderers: dict[str, type] = {}

    @classmethod
    @plugin_registerer('register_renderers')
    def register(cls, element):
        keyword, renderer = element
        if keyword in cls.__renderers:
            logging.warning('A renderer is already registered on keyword "{}"'.format(keyword))
            return

        cls.__renderers[keyword] = renderer

    @classmethod
    def get_renderer_class(cls, keyword: str) -> Callable[[...], PRenderer]:
        if keyword not in cls.__renderers:
            raise RendererNotFound(keyword)
        return cls.__renderers[keyword]


def get_renderer_class(keyword: str) -> Callable[[], PRenderer]:
    """Get the renderer class from the given keyword"""
    return RendererPluginSocket.get_renderer_class(keyword)
