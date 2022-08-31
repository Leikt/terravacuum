import logging
from typing import Optional, Callable, Any

from .renderer import PRenderer
from .plugin_system import register_plugin_socket, plugin_registerer


class RendererFactoryNotFound(Exception):
    """Exception raised when a renderer factory is requested but not found."""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = 'No renderer factory is registered to the keyword "{}"'.format(keyword)
        super().__init__(self.message)


class WrongArgumentForRendererConstructor(Exception):
    """Exception raised when the wrong arguments are passed to a renderer constructor."""

    def __init__(self, component_class: type):
        self.component_class = component_class
        self.message = 'Wrong arguments for the renderer constructor "{}"'.format(component_class)
        super().__init__(self.message)


RendererFactory = Callable[[Optional[Any]], PRenderer]
"""Function that create a component from the template data."""

RendererFactoryRegistration = tuple[str, RendererFactory]
"""Return type for the registration function"""

RendererFactoryReturn = tuple[str, dict]
"""Return type when the function uses the renderer_factory decorator"""


@register_plugin_socket
class RendererFactoryPluginSocket:
    """Plugin socket for the renderer factories."""

    __factories: dict[str, RendererFactory] = {}

    @classmethod
    @plugin_registerer('register_renderer_factories')
    def register(cls, element):
        keyword, factory = element
        if keyword in cls.__factories:
            logging.warning('A renderer factory is already registered on keyword "{}"'.format(keyword))
            return

        cls.__factories[keyword] = factory

    @classmethod
    def get_factory(cls, keyword: str) -> RendererFactory:
        if keyword not in cls.__factories:
            raise RendererFactoryNotFound(keyword)
        return cls.__factories[keyword]


def get_renderer_factory(keyword: str) -> RendererFactory:
    """Retrieve the renderer factory associated with the given keyword. Raise a ComponentFactoryNotFound error if
    it's missing."""
    return RendererFactoryPluginSocket.get_factory(keyword)
