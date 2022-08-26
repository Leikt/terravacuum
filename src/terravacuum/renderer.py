import logging
from typing import Any, Callable

from .component import PComponent
from .context import Context

Renderer = Callable[[Context, PComponent], Any]


class RendererNotFound(Exception):
    """Exception raised when a renderer is requested but not found."""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = 'No renderer is registered to the keyword "{}"'.format(keyword)
        super().__init__(self.message)


class RendererPluginSocket:
    """Plugin socket for the renderers."""

    __renderers: dict[str, Renderer] = {}

    @classmethod
    def register(cls, module):
        if not hasattr(module, 'register_renderers'):
            return
        for keyword, factory in module.register_renderers():
            if keyword in cls.__renderers:
                logging.warning('A renderer is already registered on keyword "{}"'.format(keyword))
                continue

            cls.__renderers[keyword] = factory

    @classmethod
    def get_renderer(cls, keyword: str) -> Renderer:
        if keyword not in cls.__renderers:
            raise RendererNotFound(keyword)
        return cls.__renderers[keyword]


def get_renderer(keyword: str) -> Renderer:
    """Get the renderer associated with the given keyword. Raise a RendererNotFound if it's missing"""
    return RendererPluginSocket.get_renderer(keyword)
