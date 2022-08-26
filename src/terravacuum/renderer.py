import logging
from typing import Any, Protocol

from .component import PComponent
from .context import Context


class PRenderer(Protocol):
    def render(self, context: Context, component: PComponent) -> Any:
        """Render the component."""


class RendererNotFound(Exception):
    """Exception raised when a renderer is requested but not found."""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = 'No renderer is registered to the keyword "{}"'.format(keyword)
        super().__init__(self.message)


class RendererPluginSocket:
    """Plugin socket for the renderers."""

    __renderers: dict[str, type] = {}

    @classmethod
    def register(cls, module):
        if not hasattr(module, 'register_renderers'):
            return
        for keyword, renderer in module.register_renderers():
            if keyword in cls.__renderers:
                logging.warning('A renderer is already registered on keyword "{}"'.format(keyword))
                continue

            cls.__renderers[keyword] = renderer

    @classmethod
    def get_renderer_class(cls, keyword: str) -> type:
        if keyword not in cls.__renderers:
            raise RendererNotFound(keyword)
        return cls.__renderers[keyword]


def get_renderer_class(keyword: str) -> type:
    """Get the renderer associated with the given keyword. Raise a RendererNotFound if it's missing"""
    return RendererPluginSocket.get_renderer_class(keyword)
