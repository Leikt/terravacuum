import logging
from dataclasses import dataclass
from typing import Protocol

from .plugin_system import register_plugin_socket, plugin_registerer


class ComponentNotFound(Exception):
    """Exception raised when a component is requested but not found."""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = 'No component is registered to the keyword "{}"'.format(keyword)
        super().__init__(self.message)


@dataclass
class PComponent(Protocol):
    """A component of the template, it is able to process data to a renderer"""
    renderer: str


ComponentRegistration = tuple[str, type]
"""Return type for the register_components method."""


@register_plugin_socket
class ComponentPluginSocket:
    """Plugin socket for the components."""

    __components: dict[str, type] = {}

    @classmethod
    @plugin_registerer('register_components')
    def register(cls, element):
        keyword, factory = element
        if keyword in cls.__components:
            logging.warning('A component factory is already registered on keyword "{}"'.format(keyword))
            return

        cls.__components[keyword] = factory

    @classmethod
    def get_component_class(cls, keyword: str) -> type:
        if keyword not in cls.__components:
            raise ComponentNotFound(keyword)
        return cls.__components[keyword]


def get_component_class(keyword: str) -> type:
    """Get the component associated with the given keyword. Raise a ComponentNotFound if it's missing"""
    return ComponentPluginSocket.get_component_class(keyword)
