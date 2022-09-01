from dataclasses import dataclass
from typing import Protocol

from terravacuum import PluginLoader, PluginItemNotFoundError


class ComponentNotFound(PluginItemNotFoundError):
    """Exception raised when a component is requested but not found."""


@dataclass
class PComponent(Protocol):
    """A component of the template, it is able to process data to a renderer"""
    renderer: str


ComponentRegistration = tuple[str, type]
"""Return type for the register_components method."""


def get_component_class(keyword: str) -> type:
    """Get the component associated with the given keyword. Raise a ComponentNotFound if it's missing"""
    return PluginLoader.get('component')[keyword]
