import logging
from typing import Callable

from .renderer import PRenderer

RendererFactory = Callable[[], PRenderer]
"""Callable that create a PRenderer. Generally used for the root renderer"""


class RendererFactoryNotFound(Exception):
    """Exception raised when a renderer factory is requested but not found."""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = 'No renderer factory is registered to the keyword "{}"'.format(keyword)
        super().__init__(self.message)


class RendererFactoryPluginSocket:
    """Plugin socket for the renderers factories."""

    __factories: dict[str, RendererFactory] = {}

    @classmethod
    def register(cls, module):
        if not hasattr(module, 'register_renderers'):
            return
        for keyword, renderer in module.register_renderers():
            if keyword in cls.__factories:
                logging.warning('A renderer is already registered on keyword "{}"'.format(keyword))
                continue

            cls.__factories[keyword] = renderer

    @classmethod
    def get_renderer_factory(cls, keyword: str) -> RendererFactory:
        if keyword not in cls.__factories:
            raise RendererFactoryNotFound(keyword)
        return cls.__factories[keyword]


def get_renderer_factory(keyword: str) -> RendererFactory:
    """Get the renderer factory associated with the given keyword. Raise a RendererNotFound if it's missing"""
    return RendererFactoryPluginSocket.get_renderer_factory(keyword)
